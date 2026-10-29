"""Top-level aerosmart device: two Modbus units (ventilation + heat pump)."""

from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING

from modbus_connection import ModbusTimeoutError
from modbus_connection.model import Device, Raw, UpdateReport

from .allgemein import General
from .aussentemperatur import OutsideTemperature
from .brandmeldeanlage import FireAlarm
from .carbondioxide import CarbonDioxide
from .evu import UtilityLockout
from .feinstaubfilter import FineDustFilter
from .funktionen import BoostFunctionsHeatPump, BoostFunctionsVentilation
from .grobstaubfilter import CoarseDustFilter
from .kuehlung import Cooling
from .lueftungsanlage import Ventilation
from .raumtemperatur import RoomTemperature
from .sommerautomatik import SummerBypass
from .summenstoerung import AggregateFault
from .ventilator import Fans
from .waermepumpe import HeatPump
from .warmwasser import HotWaterHeatPump, HotWaterVentilation

if TYPE_CHECKING:
    from modbus_connection import ModbusUnit

DEFAULT_UNIT_VENTILATION = 1
DEFAULT_UNIT_HEAT_PUMP = 2

MESSAGE_SPACING_SECONDS = 0.3
CONNECT_DELAY_SECONDS = 1.0

# Fast-changing operating values and fault states. Even with the device's
# one-datapoint read limit this poll completes comfortably inside its 60-second
# Home Assistant interval.
READING_COMPONENTS = (
    "general",
    "outside_temperature",
    "fire_alarm",
    "carbon_dioxide",
    "cooling",
    "ventilation",
    "room_temperature",
    "aggregate_fault",
    "fans",
    "hot_water_ventilation",
    "utility_lockout",
    "heat_pump",
    "hot_water_heat_pump",
)

VENTILATION_READING_COMPONENTS = (
    "general",
    "outside_temperature",
    "fire_alarm",
    "carbon_dioxide",
    "cooling",
    "ventilation",
    "room_temperature",
    "aggregate_fault",
    "fans",
    "hot_water_ventilation",
)

HEAT_PUMP_READING_COMPONENTS = (
    "utility_lockout",
    "heat_pump",
    "hot_water_heat_pump",
)

# Filter counters and user settings change slowly. They are separate so a
# consumer can poll them on a longer interval and refresh them immediately
# after a write.
SETTINGS_COMPONENTS = (
    "fine_dust_filter",
    "coarse_dust_filter",
    "summer_bypass",
    "boost_functions_ventilation",
    "boost_functions_heat_pump",
)

VENTILATION_SETTINGS_COMPONENTS = (
    "fine_dust_filter",
    "coarse_dust_filter",
    "summer_bypass",
    "boost_functions_ventilation",
)

HEAT_PUMP_SETTINGS_COMPONENTS = ("boost_functions_heat_pump",)

ALL_COMPONENTS = (*READING_COMPONENTS, *SETTINGS_COMPONENTS)


class AerosmartDevice(Device):
    """An aerosmart ventilation/heat-pump unit, addressed as two Modbus units.

    The physical installation exposes one Modbus TCP gateway with two station
    (slave/unit) addresses: unit 1 is the ventilation controller (also the
    system's central controller -- most fault/request flags live there), unit
    2 is the heat pump / hot-water sub-controller. This models both under one
    device object while reporting update success per functional component.
    """

    def __init__(
        self,
        unit_ventilation: ModbusUnit,
        unit_heat_pump: ModbusUnit,
    ) -> None:
        super().__init__(unit_ventilation)
        self.configure_units(unit_ventilation, unit_heat_pump)

        self.general = General(unit_ventilation)
        self.outside_temperature = OutsideTemperature(unit_ventilation)
        self.fire_alarm = FireAlarm(unit_ventilation)
        self.carbon_dioxide = CarbonDioxide(unit_ventilation)
        self.fine_dust_filter = FineDustFilter(unit_ventilation)
        self.coarse_dust_filter = CoarseDustFilter(unit_ventilation)
        self.cooling = Cooling(unit_ventilation)
        self.ventilation = Ventilation(unit_ventilation)
        self.room_temperature = RoomTemperature(unit_ventilation)
        self.summer_bypass = SummerBypass(unit_ventilation)
        self.aggregate_fault = AggregateFault(unit_ventilation)
        self.fans = Fans(unit_ventilation)
        self.boost_functions_ventilation = BoostFunctionsVentilation(unit_ventilation)
        self.hot_water_ventilation = HotWaterVentilation(unit_ventilation)

        self.utility_lockout = UtilityLockout(unit_heat_pump)
        self.heat_pump = HeatPump(unit_heat_pump)
        self.boost_functions_heat_pump = BoostFunctionsHeatPump(unit_heat_pump)
        self.hot_water_heat_pump = HotWaterHeatPump(unit_heat_pump)

    @staticmethod
    def configure_units(
        unit_ventilation: ModbusUnit, unit_heat_pump: ModbusUnit
    ) -> None:
        """Apply the timing requirements of the physical aerosmart gateway."""
        for unit in (unit_ventilation, unit_heat_pump):
            unit.set_message_spacing(MESSAGE_SPACING_SECONDS)
            unit.require_connect_delay(CONNECT_DELAY_SECONDS)

    async def async_update_readings(self) -> UpdateReport:
        """Refresh operating values and fault states by controller."""
        return await self._async_poll_controllers(
            VENTILATION_READING_COMPONENTS, HEAT_PUMP_READING_COMPONENTS
        )

    async def async_update_settings(self) -> UpdateReport:
        """Refresh slow-changing settings and filter counters by controller."""
        return await self._async_poll_controllers(
            VENTILATION_SETTINGS_COMPONENTS, HEAT_PUMP_SETTINGS_COMPONENTS
        )

    async def async_update(self) -> UpdateReport:
        """Refresh every component, preserving partial-update information."""
        report = await self.async_update_readings()
        return await self._async_poll_controllers(
            VENTILATION_SETTINGS_COMPONENTS,
            HEAT_PUMP_SETTINGS_COMPONENTS,
            report,
        )

    async def _async_poll_controllers(
        self,
        ventilation_components: tuple[str, ...],
        heat_pump_components: tuple[str, ...],
        report: UpdateReport | None = None,
    ) -> UpdateReport:
        """Poll each controller component independently when a unit times out.

        ``Device.async_poll`` raises the first timeout to identify a dead link.
        aerosmart uses independent controller units on one gateway, so a silent
        component must not prevent polling healthy ventilation or heat-pump
        components.
        """
        if report is None:
            report = UpdateReport()
        for component in ventilation_components:
            try:
                await self.async_poll((component,), report)
            except ModbusTimeoutError as err:
                report.failed[component] = err
        return await self.async_poll(heat_pump_components, report)

    async def async_read_raw(self, names: Iterable[str] = ALL_COMPONENTS) -> Raw:
        """Read undecoded register values for the selected components."""
        return await super().async_read_raw(names)
