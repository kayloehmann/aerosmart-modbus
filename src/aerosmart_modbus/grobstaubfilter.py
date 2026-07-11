"""Coarse dust filter (source: modbus/aerosmartm/grobstaubfilter.yaml)."""

from __future__ import annotations

from .model import AerosmartComponent, int32, uint32


class CoarseDustFilter(AerosmartComponent):
    """Coarse dust filter."""

    betriebsstunden_grobstaubfilter = int32(
        926,
        scale=0.0166666667,
        unit="h",
        source_key="aerosmartm_betriebsstunden_grobstaubfilter",
    )

    grobstaubfilter_vorhanden = uint32(
        5154, value_kind="boolean", source_key="aerosmartm_grobstaubfilter_vorhanden"
    )

    # Grobstaubfilter wechseln?
    grobstaubfilter_wechseln = uint32(
        7002,
        value_kind="boolean",
        source_key="aerosmartm_grobstaubfilter_wechseln",
        description="Grobstaubfilter wechseln?",
    )

    # Grobstaubfilter Standzeit
    grobstaubfilter_standzeit = uint32(
        5030,
        unit="h",
        source_key="aerosmartm_grobstaubfilter_standzeit",
        description="Grobstaubfilter Standzeit",
    )

    # Grobstaubfilter: Betriebsart Filterüberwachung
    grobstaubfilter_betriebsart_filterueberwachung = uint32(
        5164,
        source_key="aerosmartm_grobstaubfilter_betriebsart_filterueberwachung",
        description="Grobstaubfilter: Betriebsart Filterüberwachung",
    )

    # Grobstaubfilter: Maximales Fördervolumen
    grobstaubfilter_max_foerdervolume = uint32(
        5166,
        unit="m³",
        source_key="aerosmartm_grobstaubfilter_max_foerdervolume",
        description="Grobstaubfilter: Maximales Fördervolumen",
    )
