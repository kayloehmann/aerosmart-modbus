"""Cooling (source: modbus/aerosmartm/kuehlung.yaml)."""

from __future__ import annotations

from .model import AerosmartComponent, uint32


class Cooling(AerosmartComponent):
    """Cooling."""

    # Temperatur Außenluft: Kühlung aus
    aussenluft_temp_kuehlung_aus = uint32(
        5200,
        scale=0.001,
        unit="°C",
        source_key="aerosmartm_aussenluft_temp_kuehlung_aus",
        description="Temperatur Außenluft: Kühlung aus",
    )

    # Temperatur Außenluft: Kühlung ein
    aussenluft_temp_kuehlung_ein = uint32(
        5198,
        scale=0.001,
        unit="°C",
        source_key="aerosmartm_aussenluft_temp_kuehlung_ein",
        description="Temperatur Außenluft: Kühlung ein",
    )

    # Kühlung vorhanden?
    kuehlung_vorhanden = uint32(
        5192,
        value_kind="boolean",
        source_key="aerosmartm_kuehlung_vorhanden",
        description="Kühlung vorhanden?",
    )
