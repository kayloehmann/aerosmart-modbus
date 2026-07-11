"""General controller registers (source: modbus/aerosmartm/allgemein.yaml)."""

from __future__ import annotations

from .model import AerosmartComponent, uint32


class General(AerosmartComponent):
    """General controller registers."""

    # ###########################################################################
    wochentag = uint32(
        1174,
        source_key="aerosmartm_wochentag",
        description="###########################################################################",
    )

    # Software Version
    software_version = uint32(
        1156, source_key="aerosmartm_software_version", description="Software Version"
    )

    # Gerätetyp
    device_type = uint32(
        5000, source_key="aerosmartm_device_type", description="Gerätetyp"
    )

    # Relaiskontakt: EXT (LU)
    relaykontakt_ext_lu = uint32(
        252,
        value_kind="boolean",
        source_key="aerosmartm_relaykontakt_ext_lu",
        description="Relaiskontakt: EXT (LU)",
    )

    # Revisionstüre
    revisionstuer = uint32(
        226, source_key="aerosmartm_revisionstuer", description="Revisionstüre"
    )

    # Uhrzeit
    time = uint32(5212, source_key="aerosmartm_time", description="Uhrzeit")

    # Uhrzeit und Datum verschicken
    send_date_time = uint32(
        5442,
        source_key="aerosmartm_send_date_time",
        description="Uhrzeit und Datum verschicken",
    )

    # Datum
    date = uint32(5210, source_key="aerosmartm_date", description="Datum")
