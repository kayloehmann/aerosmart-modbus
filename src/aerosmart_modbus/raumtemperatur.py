"""Room temperature (source: modbus/aerosmartm/raumtemperatur.yaml)."""

from __future__ import annotations

from .model import AerosmartComponent, uint32


class RoomTemperature(AerosmartComponent):
    """Room temperature."""

    # Temperatur Raumluft
    temp_raumluft = uint32(
        200,
        scale=0.001,
        unit="°C",
        source_key="aerosmartm_temp_raumluft",
        description="Temperatur Raumluft",
    )

    # Temperatur Raumluft Soll
    temp_raumluft_soll = uint32(
        5016,
        scale=0.001,
        unit="°C",
        writable=True,
        source_key="aerosmartm_temp_raumluft_soll",
        description="Temperatur Raumluft Soll",
    )

    # Temperatur Raum Beschattung
    raum_temp_beschattung = uint32(
        5338,
        scale=0.001,
        unit="°C",
        source_key="aerosmartm_raum_temp_beschattung",
        description="Temperatur Raum Beschattung",
    )

    # Störung: Temperaturfühler Raum
    stoerung_temperaturfuehler_raum = uint32(
        804,
        value_kind="boolean",
        source_key="aerosmartm_stoerung_temperaturfuehler_raum",
        description="Störung: Temperaturfühler Raum",
    )

    # Time-Out: Solltemperatur Raum
    timeout_soll_temp_raum = uint32(
        7508,
        value_kind="boolean",
        source_key="aerosmartm_timeout_soll_temp_raum",
        description="Time-Out: Solltemperatur Raum",
    )

    # Time-Out: Temperaturfühler Raum
    timeout_temp_fuehler_raum = uint32(
        7506,
        value_kind="boolean",
        source_key="aerosmartm_timeout_temp_fuehler_raum",
        description="Time-Out: Temperaturfühler Raum",
    )

    # Anforderung: Raum-Heizstufe 1 (read)
    anforderung_raum_heizstufe_1 = uint32(
        1032,
        value_kind="boolean",
        source_key="aerosmartm_anforderung_raum_heizstufe_1",
        description="Anforderung: Raum-Heizstufe 1 (read)",
    )

    # Anforderung: Raum-Heizstufe 2 (read)
    anforderung_raum_heizstufe_2 = uint32(
        1034,
        value_kind="boolean",
        source_key="aerosmartm_anforderung_raum_heizstufe_2",
        description="Anforderung: Raum-Heizstufe 2 (read)",
    )
