"""Enum-coded aerosmart register values.

Only registers with a documented, confirmed code table go here -- guessing
enum members for a register whose codes aren't independently verified would
be worse than leaving it a plain integer.
"""

from __future__ import annotations

from enum import IntEnum


class VentilationMode(IntEnum):
    """``Betriebsart`` (address 5002), verified against the official
    Drexel & Weiss Modbus documentation (aerosmart_m_modbus.pdf,
    "Modbus_Parameter_aerosmart_m", p.55, table "aerosmart m - LU").
    """

    MANUAL_0 = 0
    MANUAL_1 = 1
    MANUAL_2 = 2
    MANUAL_3 = 3
    AUTOMATIC = 4
    PARTY = 5


class HeatPumpStatus(IntEnum):
    """``Status Wärmepumpe`` (address 1314), documented for codes 0-12.

    Source: official Drexel & Weiss Modbus documentation
    (aerosmart_m_modbus.pdf, "aerosmart m - WP", p.61).
    """

    RESTART_INHIBIT = 0
    OFF = 1
    BRINE_PUMP_LEAD_TIME = 2
    FAN_LEAD_TIME = 3
    OPEN_HOT_GAS_VALVE = 4
    OPEN_LIQUID_REFRIGERANT_VALVE = 5
    START_COMPRESSOR = 6
    MINIMUM_RUNTIME = 7
    ON = 8
    PUMP_DOWN_REFRIGERANT = 9
    PUMP_DOWN_DURING_DEFROST = 10
    DEFROSTING = 11
    DRIP_AFTER_DEFROST = 12
