"""Utility (EVU) lockout (source: modbus/aerosmartm/evu.yaml)."""

from __future__ import annotations

from .model import AerosmartComponent, uint32


class UtilityLockout(AerosmartComponent):
    """Utility (EVU) lockout."""

    # EVU Anlage vorhanden?
    evu_vorhanden = uint32(
        5146,
        value_kind="boolean",
        source_key="aerosmartm_evu_vorhanden",
        description="EVU Anlage vorhanden?",
    )

    # EVU-Sperre Brauchwasser aktiv?
    evu_sperre_brauchwasser_aktiv = uint32(
        1270,
        value_kind="boolean",
        source_key="aerosmartm_evu_sperre_brauchwasser_aktiv",
        description="EVU-Sperre Brauchwasser aktiv?",
    )

    # EVU-Sperre Elektroheizstab aktiv?
    evu_sperre_elektroheizstab_aktiv = uint32(
        1274,
        value_kind="boolean",
        source_key="aerosmartm_evu_sperre_elektroheizstab_aktiv",
        description="EVU-Sperre Elektroheizstab aktiv?",
    )

    # EVU-Sperre Raumheizung aktiv?
    evu_sperre_raumheizung_aktiv = uint32(
        1272,
        value_kind="boolean",
        source_key="aerosmartm_evu_sperre_raumheizung_aktiv",
        description="EVU-Sperre Raumheizung aktiv?",
    )
