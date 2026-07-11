"""Enum-coded aerosmart register values.

Only registers with a documented, confirmed code table go here -- guessing
enum members for a register whose codes aren't independently verified would
be worse than leaving it a plain integer (see e.g. ``wp_status`` in
waermepumpe.py, deliberately left undecoded).
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
