"""Fire alarm system (source: modbus/aerosmartm/brandmeldeanlage.yaml)."""

from __future__ import annotations

from .model import AerosmartComponent, uint32


class FireAlarm(AerosmartComponent):
    """Fire alarm system."""

    # Brandmeldealarm
    brandmeldealarm = uint32(
        838,
        value_kind="boolean",
        source_key="aerosmartm_brandmeldealarm",
        description="Brandmeldealarm",
    )

    # Brandmeldeanlage vorhanden?
    brandmeldealarm_vorhanden = uint32(
        5068,
        value_kind="boolean",
        source_key="aerosmartm_brandmeldealarm_vorhanden",
        description="Brandmeldeanlage vorhanden?",
    )

    # Kontakt: Brandmeldealarm
    kontakt_brandmeldealarm = uint32(
        238,
        value_kind="boolean",
        source_key="aerosmartm_kontakt_brandmeldealarm",
        description="Kontakt: Brandmeldealarm",
    )
