"""Smoke test: AerosmartDevice reads both units against the in-memory mock."""

import asyncio

import pytest
from modbus_connection import ModbusTimeoutError
from modbus_connection.mock import MockModbusConnection
from modbus_connection.model import UpdateReport

from aerosmart_modbus import (
    AerosmartDevice,
    UnverifiedWriteError,
    WriteVerificationError,
)
from aerosmart_modbus.aerosmart import (
    ALL_COMPONENTS,
    READING_COMPONENTS,
    SETTINGS_COMPONENTS,
)
from aerosmart_modbus.enums import HeatPumpStatus, VentilationMode


def test_device_updates_both_units():
    conn = MockModbusConnection()
    unit_v = conn.for_unit(1)
    unit_h = conn.for_unit(2)

    # uint32 spans 2 registers, big word order (high word first): a scalar
    # write like ``holding[addr] = 3`` would only set the high word (-> a
    # value shifted left by 16 bits) -- use the 2-element list form instead.
    unit_v.holding[1174] = [0, 3]  # wochentag
    unit_v.holding[202] = [0, 123]  # temp_aussenluft (scale 0.001 -> 0.123)
    unit_h.holding[1044] = [0, 1]  # waermepumpe
    unit_h.holding[1314] = [0, 1]  # wp_status: Wärmepumpe aus
    unit_h.holding[212] = [0, 45000]  # warmwasser_speicher_oben (scale 0.001 -> 45.0)

    device = AerosmartDevice(unit_v, unit_h)
    report = asyncio.run(device.async_update())

    assert report.complete
    assert device.general.wochentag == 3
    assert device.outside_temperature.temp_aussenluft == 0.123
    assert device.heat_pump.waermepumpe == 1
    assert device.heat_pump.wp_status is HeatPumpStatus.OFF
    assert device.hot_water_heat_pump.warmwasser_speicher_oben == 45.0


def test_negative_outside_air_reduction_thresholds_are_signed():
    """Confirmed negative thresholds must not wrap to about 4.3 million degrees."""
    conn = MockModbusConnection()
    unit_v = conn.for_unit(1)
    device = AerosmartDevice(unit_v, conn.for_unit(2))

    raw_10_percent = (1 << 32) - 3300
    raw_20_percent = (1 << 32) - 10300
    unit_v.holding[5422] = [raw_10_percent >> 16, raw_10_percent & 0xFFFF]
    unit_v.holding[5424] = [raw_20_percent >> 16, raw_20_percent & 0xFFFF]

    asyncio.run(device.outside_temperature.async_update())

    assert (
        device.outside_temperature.aussenluft_temp_reduktion_luftmenge_10_percent
        == -3.3
    )
    assert (
        device.outside_temperature.aussenluft_temp_reduktion_luftmenge_20_percent
        == -10.3
    )


def test_device_applies_gateway_timing_requirements():
    """Every consumer gets the gateway-safe timing from the device model."""
    conn = MockModbusConnection()
    unit_v = conn.for_unit(1)
    unit_h = conn.for_unit(2)

    AerosmartDevice(unit_v, unit_h)

    assert unit_v.message_spacing == 0.3
    assert unit_h.message_spacing == 0.3
    assert unit_v.required_connect_delay == 1.0
    assert unit_h.required_connect_delay == 1.0


def test_device_exposes_separate_poll_categories():
    conn = MockModbusConnection()
    device = AerosmartDevice(conn.for_unit(1), conn.for_unit(2))

    readings = asyncio.run(device.async_update_readings())
    settings = asyncio.run(device.async_update_settings())

    assert isinstance(readings, UpdateReport)
    assert "heat_pump" in readings.updated
    assert "general" in readings.updated
    assert "fine_dust_filter" in settings.updated
    assert "fine_dust_filter" not in readings.updated
    assert "heat_pump" not in settings.updated


def test_heat_pump_recovers_when_first_ventilation_read_times_out():
    """A failed general poll does not hide healthy controller components."""
    conn = MockModbusConnection()
    unit_v = conn.for_unit(1)
    unit_h = conn.for_unit(2)
    unit_v.fail_read(5000, ModbusTimeoutError("ventilation timeout"))
    unit_v.holding[202] = [0, 123]
    unit_h.holding[1044] = [0, 1]

    device = AerosmartDevice(unit_v, unit_h)
    report = asyncio.run(device.async_update_readings())

    assert "general" in report.failed
    assert "outside_temperature" in report.updated
    assert device.outside_temperature.temp_aussenluft == 0.123
    assert "heat_pump" in report.updated


def test_read_only_field_rejects_write():
    conn = MockModbusConnection()
    unit_v = conn.for_unit(1)
    unit_h = conn.for_unit(2)
    device = AerosmartDevice(unit_v, unit_h)

    with pytest.raises(AttributeError):
        asyncio.run(device.heat_pump.write("wp_status", 0))


def test_writable_setpoint_round_trips():
    conn = MockModbusConnection()
    unit_v = conn.for_unit(1)
    unit_h = conn.for_unit(2)
    device = AerosmartDevice(unit_v, unit_h)

    asyncio.run(device.hot_water_heat_pump.write("wp_brauchwasser_soll_temp", 50.0))
    asyncio.run(device.hot_water_heat_pump.async_update())
    assert device.hot_water_heat_pump.wp_brauchwasser_soll_temp == 50.0


@pytest.mark.parametrize(
    ("component", "field", "value", "expected"),
    (
        ("ventilation", "betriebsart", 4, VentilationMode.AUTOMATIC),
        ("room_temperature", "temp_raumluft_soll", 21.5, 21.5),
        ("hot_water_heat_pump", "wp_brauchwasser_soll_temp", 50.0, 50.0),
    ),
)
def test_verified_controls_write_and_read_back(component, field, value, expected):
    conn = MockModbusConnection()
    device = AerosmartDevice(conn.for_unit(1), conn.for_unit(2))

    actual = asyncio.run(device.async_write_verified(component, field, value))

    assert actual == expected
    assert getattr(getattr(device, component), field) == expected


def test_verified_temperature_write_is_normalized_to_register_precision():
    """A converted Fahrenheit value is verified at millidegree precision."""
    conn = MockModbusConnection()
    unit_v = conn.for_unit(1)
    device = AerosmartDevice(unit_v, conn.for_unit(2))

    actual = asyncio.run(
        device.async_write_verified(
            "room_temperature", "temp_raumluft_soll", (70 - 32) * 5 / 9
        )
    )

    assert actual == 21.111
    assert [unit_v.holding[address] for address in (5016, 5017)] == [0, 21111]
    assert device.room_temperature.temp_raumluft_soll == 21.111


async def test_poll_and_verified_write_are_serialized(monkeypatch):
    """An older in-flight poll cannot overwrite a confirmed write."""
    conn = MockModbusConnection()
    unit_v = conn.for_unit(1)
    unit_v.holding[5016] = [0, 21000]
    device = AerosmartDevice(unit_v, conn.for_unit(2))
    poll_read_started = asyncio.Event()
    release_poll_read = asyncio.Event()
    original_read = unit_v.read_holding_registers

    async def delayed_read(address, count):
        values = await original_read(address, count)
        if address == 5016 and not poll_read_started.is_set():
            poll_read_started.set()
            await release_poll_read.wait()
        return values

    monkeypatch.setattr(unit_v, "read_holding_registers", delayed_read)
    poll_task = asyncio.create_task(
        device._async_poll_controllers(("room_temperature",), ())
    )
    await poll_read_started.wait()

    write_task = asyncio.create_task(
        device.async_write_verified("room_temperature", "temp_raumluft_soll", 22.0)
    )
    await asyncio.sleep(0)
    assert not write_task.done()

    release_poll_read.set()
    await asyncio.gather(poll_task, write_task)

    assert device.room_temperature.temp_raumluft_soll == 22.0


def test_only_primary_controls_are_verified_writable():
    conn = MockModbusConnection()
    device = AerosmartDevice(conn.for_unit(1), conn.for_unit(2))

    verified = {
        (component_name, field)
        for component_name in ALL_COMPONENTS
        for field in getattr(device, component_name).resolved_fields
        if getattr(device, component_name).require_metadata_for(field).verified_writable
    }

    assert verified == {
        ("ventilation", "betriebsart"),
        ("room_temperature", "temp_raumluft_soll"),
        ("hot_water_heat_pump", "wp_brauchwasser_soll_temp"),
    }


def test_unverified_writable_register_is_rejected():
    conn = MockModbusConnection()
    unit_v = conn.for_unit(1)
    device = AerosmartDevice(unit_v, conn.for_unit(2))

    with pytest.raises(UnverifiedWriteError):
        asyncio.run(
            device.async_write_verified(
                "boost_functions_ventilation", "function_heizung_plus", 1
            )
        )

    assert 5492 not in unit_v.holding


@pytest.mark.parametrize(
    ("component", "field", "value"),
    (
        ("ventilation", "betriebsart", 6),
        ("room_temperature", "temp_raumluft_soll", 13.9),
        ("room_temperature", "temp_raumluft_soll", 26.1),
        ("hot_water_heat_pump", "wp_brauchwasser_soll_temp", 19.9),
        ("hot_water_heat_pump", "wp_brauchwasser_soll_temp", 55.1),
    ),
)
def test_verified_controls_reject_out_of_range_values(component, field, value):
    conn = MockModbusConnection()
    device = AerosmartDevice(conn.for_unit(1), conn.for_unit(2))

    with pytest.raises(ValueError):
        asyncio.run(device.async_write_verified(component, field, value))


def test_verified_write_rejects_mismatching_read_back():
    conn = MockModbusConnection()
    unit_v = conn.for_unit(1)
    device = AerosmartDevice(unit_v, conn.for_unit(2))

    def replace_written_value(event):
        if event.address == 5016:
            unit_v.holding[5017] = 22000

    unit_v.on_write(replace_written_value)

    with pytest.raises(WriteVerificationError) as error:
        asyncio.run(
            device.async_write_verified("room_temperature", "temp_raumluft_soll", 21.0)
        )

    assert error.value.requested == 21.0
    assert error.value.actual == 22.0


def test_metadata_reflects_classification():
    conn = MockModbusConnection()
    unit_v = conn.for_unit(1)
    unit_h = conn.for_unit(2)
    device = AerosmartDevice(unit_v, unit_h)

    ro = device.waermepumpe_metadata = device.heat_pump.require_metadata_for(
        "wp_status"
    )
    assert ro.value_kind == "enum"
    assert ro.enum is not None
    assert ro.enum.enum_type is HeatPumpStatus
    assert ro.enum.options[1] == (1, "Wärmepumpe aus")
    assert ro.writable is False

    rw = device.hot_water_heat_pump.require_metadata_for("wp_brauchwasser_soll_temp")
    assert rw.writable is True
    assert rw.source_key == "aerosmartm_wp_brauchwasser_soll_temp"

    flag = device.utility_lockout.require_metadata_for("evu_sperre_raumheizung_aktiv")
    assert flag.value_kind == "boolean"


def test_read_plan_never_combines_datapoints():
    """Real controllers only accept one 32-bit datapoint per request."""
    conn = MockModbusConnection()
    device = AerosmartDevice(conn.for_unit(1), conn.for_unit(2))

    for component_name in ALL_COMPONENTS:
        assert getattr(device, component_name).max_span == 2


def test_poll_categories_partition_the_register_map():
    conn = MockModbusConnection()
    device = AerosmartDevice(conn.for_unit(1), conn.for_unit(2))

    def request_count(names: tuple[str, ...]) -> int:
        return sum(
            len(blocks)
            for name in names
            for blocks in getattr(device, name)._build_plan().blocks.values()
        )

    assert set(READING_COMPONENTS).isdisjoint(SETTINGS_COMPONENTS)
    assert set(ALL_COMPONENTS) == set(READING_COMPONENTS) | set(SETTINGS_COMPONENTS)
    assert request_count(READING_COMPONENTS) == 115
    assert request_count(SETTINGS_COMPONENTS) == 22
