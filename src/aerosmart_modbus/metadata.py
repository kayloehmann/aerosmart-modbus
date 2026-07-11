"""Neutral aerosmart datapoint metadata.

This module intentionally contains no Home Assistant concepts.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

ValueKind = Literal["number", "boolean"]


@dataclass(frozen=True)
class NumberMetadata:
    """Metadata for numeric aerosmart values."""

    min_value: float | int | None = None
    max_value: float | int | None = None
    digits: int | None = None
    unit: str | None = None


@dataclass(frozen=True)
class BooleanMetadata:
    """Metadata for boolean-flavoured aerosmart values.

    aerosmart exposes every datapoint as a holding register (never a real
    Modbus coil), including ones whose meaning is inherently yes/no (Stoerung,
    Kontakt, vorhanden, ...). ``BooleanMetadata`` marks that intent so a
    consumer can build a ``binary_sensor``-style entity from a register field
    without a native ``coil()``/bool codec.
    """

    false_label: str | None = None
    true_label: str | None = None


@dataclass(frozen=True)
class DatapointMetadata:
    """Neutral metadata for one aerosmart datapoint.

    ``source_key`` is the original YAML entity id (e.g.
    ``aerosmartm_wp_status``) the field was transcribed from — kept for
    traceability back to the source Home Assistant `modbus:` config, since
    there is no manufacturer register manual to cite instead (unlike e.g.
    Trovis' HR/CL references).
    """

    value_kind: ValueKind
    source_key: str | None = None
    description: str | None = None
    writable: bool = False
    verified_writable: bool = False
    number: NumberMetadata | None = None
    boolean: BooleanMetadata | None = None


def attach_metadata(field: object, metadata: DatapointMetadata) -> object:
    """Attach aerosmart metadata to a modbus-connection field."""
    field.aerosmart_metadata = metadata  # type: ignore[attr-defined]
    return field
