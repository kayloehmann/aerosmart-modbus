"""Fans (source: modbus/aerosmartm/ventilator.yaml)."""

from __future__ import annotations

from .model import AerosmartComponent, uint32


class Fans(AerosmartComponent):
    """Fans."""

    # ###########################################################################
    ist_ventilator_zuluft = uint32(
        1184,
        unit="rpm",
        source_key="aerosmartm_ist_ventilator_zuluft",
        description="###########################################################################",
    )

    ist_ventilator_abluft = uint32(
        1186, unit="rpm", source_key="aerosmartm_ist_ventilator_abluft"
    )

    betriebsstunden_abluftventilator = uint32(
        902,
        scale=0.0166666667,
        unit="h",
        source_key="aerosmartm_betriebsstunden_abluftventilator",
    )

    betriebsstunden_zuluftventilator = uint32(
        900,
        scale=0.0166666667,
        unit="h",
        source_key="aerosmartm_betriebsstunden_zuluftventilator",
    )

    # Anforderung der Ventilatoren durch Wärmepumpe (read)
    anforderung_ventilatoren_durch_waermepumpe = uint32(
        1292,
        value_kind="boolean",
        source_key="aerosmartm_anforderung_ventilatoren_durch_waermepumpe",
        description="Anforderung der Ventilatoren durch Wärmepumpe (read)",
    )

    # Anforderung der Ventilatoren durch Zonenregelung (read)
    anforderung_ventilatoren_durch_zonenregelung = uint32(
        1336,
        value_kind="boolean",
        source_key="aerosmartm_anforderung_ventilatoren_durch_zonenregelung",
        description="Anforderung der Ventilatoren durch Zonenregelung (read)",
    )

    # Drehzahl Abluftventilator
    drehzahl_abluftventilator = uint32(
        1094,
        source_key="aerosmartm_drehzahl_abluftventilator",
        description="Drehzahl Abluftventilator",
    )

    # Drehzahl Zuluftventilator
    drehzahl_zuluftventilator = uint32(
        1092,
        source_key="aerosmartm_drehzahl_zuluftventilator",
        description="Drehzahl Zuluftventilator",
    )

    # Störung: Zuluftventilator
    stoerung_zuluftventilator = uint32(
        824,
        value_kind="boolean",
        source_key="aerosmartm_stoerung_zuluftventilator",
        description="Störung: Zuluftventilator",
    )

    # Störung: Abluftventilator
    stoerung_abluftventilator = uint32(
        826,
        value_kind="boolean",
        source_key="aerosmartm_stoerung_abluftventilator",
        description="Störung: Abluftventilator",
    )

    # Maximal zulässige Drehzahl Abluftventilator
    max_permissible_exhaust_air_fan_speed = uint32(
        5270,
        unit="1/min",
        source_key="aerosmartm_max_permissible_exhaust_air_fan_speed",
        description="Maximal zulässige Drehzahl Abluftventilator",
    )

    # Maximal zulässige Drehzahl Zuluftventilator
    max_permissible_supply_air_fan_speed = uint32(
        5268,
        unit="1/min",
        source_key="aerosmartm_max_permissible_supply_air_fan_speed",
        description="Maximal zulässige Drehzahl Zuluftventilator",
    )
