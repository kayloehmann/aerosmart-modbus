"""aerosmart_modbus -- a typed Modbus device model for aerosmart units.

Backend-neutral: built on ``modbus_connection.model``, so it runs over
pymodbus, tmodbus, or the in-memory mock. Consumed by a Home Assistant
integration in a separate repository; this package itself has no Home
Assistant dependency.
"""

from __future__ import annotations

from .aerosmart import DEFAULT_UNIT_HEAT_PUMP, DEFAULT_UNIT_VENTILATION, AerosmartDevice
from .metadata import BooleanMetadata, DatapointMetadata, NumberMetadata

__all__ = [
    "DEFAULT_UNIT_HEAT_PUMP",
    "DEFAULT_UNIT_VENTILATION",
    "AerosmartDevice",
    "BooleanMetadata",
    "DatapointMetadata",
    "NumberMetadata",
]
