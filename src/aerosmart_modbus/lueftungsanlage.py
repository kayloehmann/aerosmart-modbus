"""Ventilation unit (source: modbus/aerosmartm/lueftungsanlage.yaml)."""

from __future__ import annotations

from .model import AerosmartComponent, uint32


class Ventilation(AerosmartComponent):
    """Ventilation unit."""

    # Absenkung der Lüfterstufe 1
    absenkung_aktive_luefterstufe = uint32(
        5328,
        unit="%",
        source_key="aerosmartm_absenkung_aktive_luefterstufe",
        description="Absenkung der Lüfterstufe 1",
    )

    # Aktive Lüfterstufe
    aktive_luefterstufe = uint32(
        1066,
        source_key="aerosmartm_aktive_luefterstufe",
        description="Aktive Lüfterstufe",
    )

    # Betriebsart
    betriebsart = uint32(
        5002, source_key="aerosmartm_betriebsart", description="Betriebsart"
    )

    betriebsstunden_beschattung = uint32(
        964,
        scale=0.0166666667,
        unit="h",
        source_key="aerosmartm_betriebsstunden_beschattung",
    )

    betriebsstunden_frostschutzeinrichtung = uint32(
        940,
        scale=0.0166666667,
        unit="h",
        source_key="aerosmartm_betriebsstunden_frostschutzeinrichtung",
    )

    betriebsstunden_heizstufe1 = uint32(
        912,
        scale=0.0166666667,
        unit="h",
        source_key="aerosmartm_betriebsstunden_heizstufe1",
    )

    betriebsstunden_heizstufe2 = uint32(
        914,
        scale=0.0166666667,
        unit="h",
        source_key="aerosmartm_betriebsstunden_heizstufe2",
    )

    betriebsstunden_luefterstufe0 = uint32(
        962,
        scale=0.0166666667,
        unit="h",
        source_key="aerosmartm_betriebsstunden_luefterstufe0",
    )

    betriebsstunden_luefterstufe1 = uint32(
        904,
        scale=0.0166666667,
        unit="h",
        source_key="aerosmartm_betriebsstunden_luefterstufe1",
    )

    betriebsstunden_luefterstufe2 = uint32(
        906,
        scale=0.0166666667,
        unit="h",
        source_key="aerosmartm_betriebsstunden_luefterstufe2",
    )

    betriebsstunden_luefterstufe3 = uint32(
        908,
        scale=0.0166666667,
        unit="h",
        source_key="aerosmartm_betriebsstunden_luefterstufe3",
    )

    # Anforderung: Abtauen (read)
    anforderung_abtauen = uint32(
        1050,
        value_kind="boolean",
        source_key="aerosmartm_anforderung_abtauen",
        description="Anforderung: Abtauen (read)",
    )

    # Anforderung: Beschattung (read)
    anforderung_beschattung = uint32(
        1218,
        value_kind="boolean",
        source_key="aerosmartm_anforderung_beschattung",
        description="Anforderung: Beschattung (read)",
    )

    # Anforderung: LST3_EXT (read)
    anforderung_st3_ext = uint32(
        228,
        value_kind="boolean",
        source_key="aerosmartm_anforderung_st3_ext",
        description="Anforderung: LST3_EXT (read)",
    )

    # Beschattungsfunktion
    beschattungsfunktion = uint32(
        5336,
        source_key="aerosmartm_beschattungsfunktion",
        description="Beschattungsfunktion",
    )

    # Erhöhung der Lüfterstufe 3 (R/W)
    # Official Drexel & Weiss doc confirms R/W, 30-100 %.
    erhoehung_luefterstufe_3 = uint32(
        5330,
        unit="%",
        writable=True,
        min_value=30,
        max_value=100,
        source_key="aerosmartm_erhoehung_luefterstufe_3",
        description="Erhöhung der Lüfterstufe 3 (R/W)",
    )

    # Störung: Teilnehmer nicht erreichbar!
    stoerung_teilnehmer_nicht_erreichbar = uint32(
        856,
        value_kind="boolean",
        source_key="aerosmartm_stoerung_teilnehmer_nicht_erreichbar",
        description="Störung: Teilnehmer nicht erreichbar!",
    )

    # Störung: Temperaturfühler Verdampferregister
    stoerung_temperaturfuehler_verdampferregister = uint32(
        808,
        value_kind="boolean",
        source_key="aerosmartm_stoerung_temperaturfuehler_verdampferregister",
        description="Störung: Temperaturfühler Verdampferregister",
    )

    # Störung: Wärmepumpe Hochdruck
    stoerung_waermepumpe_hochdruck = uint32(
        818,
        value_kind="boolean",
        source_key="aerosmartm_stoerung_waermepumpe_hochdruck",
        description="Störung: Wärmepumpe Hochdruck",
    )

    # Störung: Wärmepumpe Niederdruck
    stoerung_waermepumpe_niederdruck = uint32(
        820,
        value_kind="boolean",
        source_key="aerosmartm_stoerung_waermepumpe_niederdruck",
        description="Störung: Wärmepumpe Niederdruck",
    )

    # Störung: Wert nicht zulässig
    stoerung_wert_nicht_zulaessig = uint32(
        840,
        value_kind="boolean",
        source_key="aerosmartm_stoerung_wert_nicht_zulaessig",
        description="Störung: Wert nicht zulässig",
    )

    # Gesamt beförderte Kubikmeter
    befoerderte_kubikmeter = uint32(
        946,
        unit="m³",
        source_key="aerosmartm_befoerderte_kubikmeter",
        description="Gesamt beförderte Kubikmeter",
    )

    # Gesamt beförderte Luftmenge seit Filterwechsel
    befoerderte_luftmenge_seit_filterwechsel = uint32(
        960,
        unit="m³",
        source_key="aerosmartm_befoerderte_luftmenge_seit_filterwechsel",
        description="Gesamt beförderte Luftmenge seit Filterwechsel",
    )

    # Soll-Volumenstrom Abluft
    soll_volumenstrom_abluft = uint32(
        1084,
        unit="m³",
        source_key="aerosmartm_soll_volumenstrom_abluft",
        description="Soll-Volumenstrom Abluft",
    )

    # Soll-Volumenstrom Lüfterstufe 2 (read/write)
    # Official Drexel & Weiss doc confirms R/W, 40-300 m³/h.
    soll_volumenstrom_luefterstufe2 = uint32(
        5060,
        unit="m³/h",
        writable=True,
        min_value=40,
        max_value=300,
        source_key="aerosmartm_soll_volumenstrom_luefterstufe2",
        description="Soll-Volumenstrom Lüfterstufe 2 (read/write)",
    )

    # Soll-Volumenstrom Zuluft
    soll_volumenstrom_zuluft = uint32(
        1082,
        unit="m³",
        source_key="aerosmartm_soll_volumenstrom_zuluft",
        description="Soll-Volumenstrom Zuluft",
    )

    # Volumenstrombalance ZuluftAbluft
    volumenstrombalance_zuluftabluft = uint32(
        5026,
        unit="%",
        source_key="aerosmartm_volumenstrombalance_zuluftabluft",
        description="Volumenstrombalance ZuluftAbluft",
    )
