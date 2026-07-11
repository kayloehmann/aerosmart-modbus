"""Fine dust filter (source: modbus/aerosmartm/feinstaubfilter.yaml)."""

from __future__ import annotations

from .model import AerosmartComponent, uint32


class FineDustFilter(AerosmartComponent):
    """Fine dust filter."""

    # Feinstaubfilter vorhanden?
    feinstaubfilter_vorhanden = uint32(
        5034,
        value_kind="boolean",
        source_key="aerosmartm_feinstaubfilter_vorhanden",
        description="Feinstaubfilter vorhanden?",
    )

    # Feinstaubfilter wechseln?
    feinstaubfilter_wechseln = uint32(
        7004,
        value_kind="boolean",
        source_key="aerosmartm_feinstaubfilter_wechseln",
        description="Feinstaubfilter wechseln?",
    )

    # Feinstaubfilter Standzeit
    feinstaubfilter_standzeit = uint32(
        5032,
        unit="h",
        source_key="aerosmartm_feinstaubfilter_standzeit",
        description="Feinstaubfilter Standzeit",
    )

    betriebsstunden_feinstaubfilter = uint32(
        928,
        scale=0.0166666667,
        unit="h",
        source_key="aerosmartm_betriebsstunden_feinstaubfilter",
    )
