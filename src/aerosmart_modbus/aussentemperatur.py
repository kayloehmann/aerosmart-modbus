"""Outside air temperature (source: modbus/aerosmartm/aussentemperatur.yaml)."""

from __future__ import annotations

from .model import AerosmartComponent, uint32


class OutsideTemperature(AerosmartComponent):
    """Outside air temperature."""

    # Außenluftfühler vorhanden?
    aussenluftfuehler_vorhanden = uint32(
        5304,
        value_kind="boolean",
        source_key="aerosmartm_aussenluftfuehler_vorhanden",
        description="Außenluftfühler vorhanden?",
    )

    # Temperatur Aussenluft
    temp_aussenluft = uint32(
        202,
        scale=0.001,
        unit="°C",
        source_key="aerosmartm_temp_aussenluft",
        description="Temperatur Aussenluft",
    )

    # Temperatur Aussenluft: Beschattung
    aussenluft_temp_beschattung = uint32(
        5340,
        scale=0.001,
        unit="°C",
        source_key="aerosmartm_aussenluft_temp_beschattung",
        description="Temperatur Aussenluft: Beschattung",
    )

    # Temperatur Außenluft: Frostschutz
    aussenluft_temp_frostschutz = uint32(
        5206,
        scale=0.001,
        unit="°C",
        source_key="aerosmartm_aussenluft_temp_frostschutz",
        description="Temperatur Außenluft: Frostschutz",
    )

    # Temperatur Außenluft: Frostschutz aus
    aussenluft_temp_frostschutz_aus = uint32(
        5090,
        scale=0.001,
        unit="°C",
        source_key="aerosmartm_aussenluft_temp_frostschutz_aus",
        description="Temperatur Außenluft: Frostschutz aus",
    )

    # Temperatur Außenluft: Frostschutz ein
    aussenluft_temp_frostschutz_ein = uint32(
        5088,
        scale=0.001,
        unit="°C",
        source_key="aerosmartm_aussenluft_temp_frostschutz_ein",
        description="Temperatur Außenluft: Frostschutz ein",
    )

    # Temperatur Außenluft: Reduktion Luftmenge 10%
    aussenluft_temp_reduktion_luftmenge_10_percent = uint32(
        5422,
        scale=0.001,
        unit="°C",
        source_key="aerosmartm_aussenluft_temp_reduktion_luftmenge_10_percent",
        description="Temperatur Außenluft: Reduktion Luftmenge 10%",
    )

    # Temperatur Außenluft: Reduktion Luftmenge 20%
    aussenluft_temp_reduktion_luftmenge_20_percent = uint32(
        5424,
        scale=0.001,
        unit="°C",
        source_key="aerosmartm_aussenluft_temp_reduktion_luftmenge_20_percent",
        description="Temperatur Außenluft: Reduktion Luftmenge 20%",
    )

    # Temperatur Außenluft: Sommerautomatik aktivieren
    aussenluft_temp_sommerautomatik_aktivieren = uint32(
        5386,
        scale=0.001,
        unit="°C",
        source_key="aerosmartm_aussenluft_temp_sommerautomatik_aktivieren",
        description="Temperatur Außenluft: Sommerautomatik aktivieren",
    )

    # Temperatur Außenluft: Sommerautomatik deaktivieren
    aussenluft_temp_sommerautomatik_deaktivieren = uint32(
        5388,
        scale=0.001,
        unit="°C",
        source_key="aerosmartm_aussenluft_temp_sommerautomatik_deaktivieren",
        description="Temperatur Außenluft: Sommerautomatik deaktivieren",
    )

    # Temperatur: Sole nach Außenluftvorwärmung
    aussenluft_temp_sole_nach_aussenluftvorwaermung = uint32(
        206,
        scale=0.001,
        unit="°C",
        source_key="aerosmartm_aussenluft_temp_sole_nach_aussenluftvorwaermung",
        description="Temperatur: Sole nach Außenluftvorwärmung",
    )

    # Temperaturschwelle Außenluft \\ Heizen / Kühlen
    aussenluft_temp_schwelle_heizen_kuehlen = uint32(
        5186,
        scale=0.001,
        unit="°C",
        source_key="aerosmartm_aussenluft_temp_schwelle_heizen_kuehlen",
        description="Temperaturschwelle Außenluft \\\\ Heizen / Kühlen",
    )

    # Vereisungsschutz
    vereisungsschutz = uint32(
        1294, source_key="aerosmartm_vereisungsschutz", description="Vereisungsschutz"
    )

    # Störung: Temperaturfühler Außenluft
    stoerung_temperaturfuehler_aussenluft = uint32(
        806,
        value_kind="boolean",
        source_key="aerosmartm_stoerung_temperaturfuehler_aussenluft",
        description="Störung: Temperaturfühler Außenluft",
    )

    # Störung: Temperaturfühler Sole Außenluft
    stoerung_temperaturfuehler_sole_aussenluft = uint32(
        7504,
        value_kind="boolean",
        source_key="aerosmartm_stoerung_temperaturfuehler_sole_aussenluft",
        description="Störung: Temperaturfühler Sole Außenluft",
    )

    # Betriebsstunden Solekreis Außenluft
    betriebsstunden_sole_kreis_aussenluft = uint32(
        970,
        scale=0.0166666667,
        unit="h",
        source_key="aerosmartm_betriebsstunden_sole_kreis_aussenluft",
        description="Betriebsstunden Solekreis Außenluft",
    )
