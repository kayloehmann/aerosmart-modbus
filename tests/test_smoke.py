"""Smoke test: AerosmartDevice reads both units against the in-memory mock."""

import asyncio

import pytest
from modbus_connection.mock import MockModbusConnection

from aerosmart_modbus import AerosmartDevice


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
    unit_h.holding[212] = [0, 45000]  # warmwasser_speicher_oben (scale 0.001 -> 45.0)

    device = AerosmartDevice(unit_v, unit_h)
    asyncio.run(device.async_update())

    assert device.general.wochentag == 3
    assert device.outside_temperature.temp_aussenluft == 0.123
    assert device.heat_pump.waermepumpe == 1
    assert device.hot_water_heat_pump.warmwasser_speicher_oben == 45.0


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


def test_metadata_reflects_classification():
    conn = MockModbusConnection()
    unit_v = conn.for_unit(1)
    unit_h = conn.for_unit(2)
    device = AerosmartDevice(unit_v, unit_h)

    ro = device.waermepumpe_metadata = device.heat_pump.require_metadata_for(
        "wp_status"
    )
    assert ro.value_kind == "number"
    assert ro.writable is False

    rw = device.hot_water_heat_pump.require_metadata_for("wp_brauchwasser_soll_temp")
    assert rw.writable is True
    assert rw.source_key == "aerosmartm_wp_brauchwasser_soll_temp"

    flag = device.utility_lockout.require_metadata_for("evu_sperre_raumheizung_aktiv")
    assert flag.value_kind == "boolean"
