"""Aggregate fault (source: modbus/aerosmartm/summenstoerung.yaml)."""

from __future__ import annotations

from .model import AerosmartComponent, uint32


class AggregateFault(AerosmartComponent):
    """Aggregate fault."""

    # Störung: Summenstörung
    stoerung_summenstoerung = uint32(
        800,
        value_kind="boolean",
        source_key="aerosmartm_stoerung_summenstoerung",
        description="Störung: Summenstörung",
    )

    # Störung: Summenstörung 2
    stoerung_summenstoerung2 = uint32(
        7500,
        value_kind="boolean",
        source_key="aerosmartm_stoerung_summenstoerung2",
        description="Störung: Summenstörung 2",
    )
