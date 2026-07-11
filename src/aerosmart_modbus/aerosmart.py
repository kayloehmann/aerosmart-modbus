"""Top-level aerosmart device: two Modbus units (ventilation + heat pump)."""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from modbus_connection.model import ComponentGroup

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


class AerosmartDevice:
    """An aerosmart ventilation/heat-pump unit, addressed as two Modbus units.

    The physical installation exposes one Modbus TCP gateway with two station
    (slave/unit) addresses: unit 1 is the ventilation controller (also the
    system's central controller -- most fault/request flags live there), unit
    2 is the heat pump / hot-water sub-controller. This models both under one
    device object, each polled with its own pooled ``ComponentGroup``.
    """

    def __init__(
        self,
        unit_ventilation: ModbusUnit,
        unit_heat_pump: ModbusUnit,
    ) -> None:
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

        self._group_ventilation = ComponentGroup(
            unit_ventilation,
            [
                self.general,
                self.outside_temperature,
                self.fire_alarm,
                self.carbon_dioxide,
                self.fine_dust_filter,
                self.coarse_dust_filter,
                self.cooling,
                self.ventilation,
                self.room_temperature,
                self.summer_bypass,
                self.aggregate_fault,
                self.fans,
                self.boost_functions_ventilation,
                self.hot_water_ventilation,
            ],
        )
        self._group_heat_pump = ComponentGroup(
            unit_heat_pump,
            [
                self.utility_lockout,
                self.heat_pump,
                self.boost_functions_heat_pump,
                self.hot_water_heat_pump,
            ],
        )

    async def async_update(self) -> None:
        """Refresh both units' components concurrently."""
        await asyncio.gather(
            self._group_ventilation.async_update(),
            self._group_heat_pump.async_update(),
        )
