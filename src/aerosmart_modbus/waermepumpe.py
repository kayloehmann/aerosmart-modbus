"""Heat pump (source: modbus/aerosmartm/waermepumpe.yaml)."""

from __future__ import annotations

from .enums import HeatPumpStatus
from .model import AerosmartComponent, enum, uint32


class HeatPump(AerosmartComponent):
    """Heat pump."""

    # Wärmepumpe
    waermepumpe = uint32(
        1044, source_key="aerosmartm_waermepumpe", description="Wärmepumpe"
    )

    # Verdampferregister
    wp_verdamperregister = uint32(
        210,
        scale=100,
        unit="°C",
        source_key="aerosmartm_wp_verdamperregister",
        description="Verdampferregister",
    )

    # Zentralgerät Adresse (WP)
    wp_zentralgeraet_adresse = uint32(
        5436,
        source_key="aerosmartm_wp_zentralgeraet_adresse",
        description="Zentralgerät Adresse (WP)",
    )

    # Betriebsstunden: Kompressormotor
    wp_betriebsstunden_kompressormotor = uint32(
        910,
        unit="h",
        source_key="aerosmartm_wp_betriebsstunden_kompressormotor",
        description="Betriebsstunden: Kompressormotor",
    )

    # Betriebsstunden: Magnetventil Flüssiggas
    wp_betriebsstunden_magnetventil_fluessiggas = uint32(
        916,
        unit="h",
        source_key="aerosmartm_wp_betriebsstunden_magnetventil_fluessiggas",
        description="Betriebsstunden: Magnetventil Flüssiggas",
    )

    # Betriebsstunden: Magnetventil Heißgas
    wp_betriebsstunden_magnetventil_heissgas = uint32(
        918,
        unit="h",
        source_key="aerosmartm_wp_betriebsstunden_magnetventil_heissgas",
        description="Betriebsstunden: Magnetventil Heißgas",
    )

    # Betriebsstunden: Magnetventil Luftkondensator
    wp_betriebsstunden_magnetventil_luftkondensator = uint32(
        920,
        unit="h",
        source_key="aerosmartm_wp_betriebsstunden_magnetventil_luftkondensator",
        description="Betriebsstunden: Magnetventil Luftkondensator",
    )

    # Hochdruck Wärmepumpe
    wp_hochdruck = uint32(
        222, source_key="aerosmartm_wp_hochdruck", description="Hochdruck Wärmepumpe"
    )

    # Kontakt (EVU)
    wp_kontakt_evu = uint32(
        232,
        value_kind="boolean",
        source_key="aerosmartm_wp_kontakt_evu",
        description="Kontakt (EVU)",
    )

    # Niederdruck Wärmepumpe
    wp_niederdruck = uint32(
        224,
        source_key="aerosmartm_wp_niederdruck",
        description="Niederdruck Wärmepumpe",
    )

    # Relaiskontakt: EXT (WP)
    wp_relaiskontakt_ext = uint32(
        262,
        value_kind="boolean",
        source_key="aerosmartm_wp_relaiskontakt_ext",
        description="Relaiskontakt: EXT (WP)",
    )

    # Status Wärmepumpe
    wp_status = enum(
        1314,
        HeatPumpStatus,
        options=(
            (0, "Wiedereinschaltsperre"),
            (1, "Wärmepumpe aus"),
            (2, "Vorlaufzeit Solepumpe"),
            (3, "Vorlaufzeit Ventilatoren"),
            (4, "Öffnen Heißgasventil"),
            (5, "Öffnen Flüssiggasventil"),
            (6, "Start Kompressor"),
            (7, "Mindestlaufzeit Wärmepumpe"),
            (8, "Wärmepumpe ein"),
            (9, "Kältemittel absaugen"),
            (10, "Beim Abtauen absaugen"),
            (11, "Abtauen ein"),
            (12, "Nach Abtauen abtropfen"),
        ),
        source_key="aerosmartm_wp_status",
        description="Status Wärmepumpe",
    )

    # Status Wärmepumpe (Restzeit des aktuellen Status)
    wp_status_restlaufzeit = uint32(
        1316,
        source_key="aerosmartm_wp_status_restlaufzeit",
        description="Status Wärmepumpe (Restzeit des aktuellen Status)",
    )
