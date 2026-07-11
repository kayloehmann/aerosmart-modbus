"""Domestic hot water (source: modbus/aerosmartm/warmwasser.yaml)."""

from __future__ import annotations

from .model import AerosmartComponent, uint32


class HotWaterVentilation(AerosmartComponent):
    """Domestic hot water (ventilation unit registers)."""

    # Anforderung Disbalance (Boilerüberwärmung) (read)
    anforderung_disbalance_boilerueberwaermung = uint32(
        1338,
        value_kind="boolean",
        source_key="aerosmartm_anforderung_disbalance_boilerueberwaermung",
        description="Anforderung Disbalance (Boilerüberwärmung) (read)",
    )

    # Störung: Boilerfühler Elektroheizstab
    stoerung_elektroheizstab = uint32(
        828,
        value_kind="boolean",
        source_key="aerosmartm_stoerung_elektroheizstab",
        description="Störung: Boilerfühler Elektroheizstab",
    )

    # Störung: Boilerfühler Wärmepumpe
    stoerung_boilerfuehler_waermepumpe = uint32(
        830,
        value_kind="boolean",
        source_key="aerosmartm_stoerung_boilerfuehler_waermepumpe",
        description="Störung: Boilerfühler Wärmepumpe",
    )

    # Störung: Boilerübertemperatur
    stoerung_boiler_uebertemperatur = uint32(
        810,
        value_kind="boolean",
        source_key="aerosmartm_stoerung_boiler_uebertemperatur",
        description="Störung: Boilerübertemperatur",
    )

    # Anforderung: Brauchwasserheizung Elektoheizstab (read)
    anforderung_brauchwasserheizung_elektroheizstab = uint32(
        1038,
        value_kind="boolean",
        source_key="aerosmartm_anforderung_brauchwasserheizung_elektroheizstab",
        description="Anforderung: Brauchwasserheizung Elektoheizstab (read)",
    )

    # Anforderung: Brauchwasserheizung Wärmepumpe (read)
    anforderung_brauchwasserheizung_waermepumpe = uint32(
        1036,
        value_kind="boolean",
        source_key="aerosmartm_anforderung_brauchwasserheizung_waermepumpe",
        description="Anforderung: Brauchwasserheizung Wärmepumpe (read)",
    )


class HotWaterHeatPump(AerosmartComponent):
    """Domestic hot water (heat pump unit registers)."""

    # Temperatur: Warmwasserspeicher oben (T_BW_EHZ)
    warmwasser_speicher_oben = uint32(
        212,
        scale=0.001,
        unit="°C",
        source_key="aerosmartm_warmwasser_speicher_oben",
        description="Temperatur: Warmwasserspeicher oben (T_BW_EHZ)",
    )

    # Temperatur: Warmwasserspeicher Wärmepumpe (T_BW_WP)
    warmwasser_warmepumpe = uint32(
        214,
        scale=0.001,
        unit="°C",
        source_key="aerosmartm_warmwasser_warmepumpe",
        description="Temperatur: Warmwasserspeicher Wärmepumpe (T_BW_WP)",
    )

    # Überschreitung Boilertemperatur
    ueberschreitung_boilertemp = uint32(
        7006,
        source_key="aerosmartm_ueberschreitung_boilertemp",
        description="Überschreitung Boilertemperatur",
    )

    # Vorübergehende Boilerübertemperatur
    wp_vorruebergehende_boilertemperatur = uint32(
        1212,
        source_key="aerosmartm_wp_vorruebergehende_boilertemperatur",
        description="Vorübergehende Boilerübertemperatur",
    )

    # Brauchwasser Solltemperatur
    wp_brauchwasser_soll_temp = uint32(
        5064,
        scale=0.001,
        unit="°C",
        writable=True,
        source_key="aerosmartm_wp_brauchwasser_soll_temp",
        description="Brauchwasser Solltemperatur",
    )

    # Brauchwassertemperatur: Raumheizungssperre
    wp_brauchwasser_temp_raumheizungssperre = uint32(
        5130,
        scale=0.001,
        unit="°C",
        source_key="aerosmartm_wp_brauchwasser_temp_raumheizungssperre",
        description="Brauchwassertemperatur: Raumheizungssperre",
    )

    # Verzögerung Brauchwassererheizung
    wp_verzoegerung_brauchwasserheizung = uint32(
        5374,
        source_key="aerosmartm_wp_verzoegerung_brauchwasserheizung",
        description="Verzögerung Brauchwassererheizung",
    )

    # Betriebsstunden: Elektroheizstab
    wp_betriebsstunden_elektroheizstab = uint32(
        922,
        unit="h",
        source_key="aerosmartm_wp_betriebsstunden_elektroheizstab",
        description="Betriebsstunden: Elektroheizstab",
    )

    # Elektroheizstab vorhanden?
    wp_elektroheizstab_vorhanden = uint32(
        5126,
        value_kind="boolean",
        source_key="aerosmartm_wp_elektroheizstab_vorhanden",
        description="Elektroheizstab vorhanden?",
    )
