"""aerosmart-specific pieces layered on the ``modbus_connection.model`` framework."""

from __future__ import annotations

from enum import IntEnum
from typing import Any

from modbus_connection.model import Component
from modbus_connection.model import enum as _modbus_enum
from modbus_connection.model import int32 as _modbus_int32
from modbus_connection.model import uint32 as _modbus_uint32

from .metadata import (
    BooleanMetadata,
    DatapointMetadata,
    EnumMetadata,
    NumberMetadata,
    attach_metadata,
)

# Every aerosmart datapoint observed so far is a 32-bit holding register
# (`input_type: holding`, `data_type: uint32`/`int32` in the source Home
# Assistant `modbus:` YAML) -- there is no 16-bit/float/string variant known
# yet, so `uint32`/`int32`/`enum` are the field factories this module exposes.
# Extend here if a future register turns out to need something else.


def uint32(
    address: int,
    *,
    scale: float = 1.0,
    unit: str | None = None,
    writable: bool = False,
    value_kind: str = "number",
    source_key: str | None = None,
    description: str | None = None,
    min_value: float | int | None = None,
    max_value: float | int | None = None,
    digits: int | None = None,
    **kwargs: Any,
):
    """An unsigned 32-bit aerosmart register, with neutral metadata attached."""
    field = _modbus_uint32(address, scale=scale, unit=unit, writable=writable, **kwargs)
    return attach_metadata(
        field,
        DatapointMetadata(
            value_kind=value_kind,  # type: ignore[arg-type]
            source_key=source_key,
            description=description,
            writable=writable,
            number=NumberMetadata(
                min_value=min_value, max_value=max_value, digits=digits, unit=unit
            )
            if value_kind == "number"
            else None,
            boolean=BooleanMetadata() if value_kind == "boolean" else None,
        ),
    )


def int32(
    address: int,
    *,
    scale: float = 1.0,
    unit: str | None = None,
    writable: bool = False,
    value_kind: str = "number",
    source_key: str | None = None,
    description: str | None = None,
    min_value: float | int | None = None,
    max_value: float | int | None = None,
    digits: int | None = None,
    **kwargs: Any,
):
    """A signed 32-bit aerosmart register, with neutral metadata attached."""
    field = _modbus_int32(address, scale=scale, unit=unit, writable=writable, **kwargs)
    return attach_metadata(
        field,
        DatapointMetadata(
            value_kind=value_kind,  # type: ignore[arg-type]
            source_key=source_key,
            description=description,
            writable=writable,
            number=NumberMetadata(
                min_value=min_value, max_value=max_value, digits=digits, unit=unit
            )
            if value_kind == "number"
            else None,
            boolean=BooleanMetadata() if value_kind == "boolean" else None,
        ),
    )


def enum[E: IntEnum](
    address: int,
    enum_type: type[E],
    *,
    count: int = 2,
    writable: bool = False,
    source_key: str | None = None,
    description: str | None = None,
    options: tuple[tuple[int, str], ...] | None = None,
    **kwargs: Any,
):
    """An enum-coded aerosmart register, with neutral metadata attached.

    ``count=2`` by default: every enum register observed so far is 32-bit
    like the rest of this device's registers, not modbus_connection's 16-bit
    default for ``enum()``. ``options`` are ``(code, label)`` pairs in
    document order; if omitted, derived from ``enum_type``'s members.
    """
    field = _modbus_enum(address, enum_type, count=count, writable=writable, **kwargs)
    resolved_options = options or tuple(
        (int(member), member.name) for member in enum_type
    )
    return attach_metadata(
        field,
        DatapointMetadata(
            value_kind="enum",
            source_key=source_key,
            description=description,
            writable=writable,
            enum=EnumMetadata(enum_type=enum_type, options=resolved_options),
        ),
    )


class AerosmartComponent(Component):
    """An aerosmart sub-system: shared read-batching limits.

    No model-variant handling (``register_ranges``/``ranges_for_model``) --
    unlike the multi-model Trovis library, only one known aerosmart
    installation backs this library so far; add ranges/variants if a second,
    differently-addressed unit ever needs supporting.
    """

    def metadata_for(self, field: str) -> DatapointMetadata | None:
        """Return neutral aerosmart metadata for a field."""
        descriptor = self._register_fields.get(field)
        if descriptor is None:
            return None
        return getattr(descriptor, "aerosmart_metadata", None)

    def require_metadata_for(self, field: str) -> DatapointMetadata:
        """Return aerosmart metadata for a field or raise."""
        metadata = self.metadata_for(field)
        if metadata is None:
            raise AttributeError(f"unknown or untyped aerosmart field {field!r}")
        return metadata
