"""Boost functions (HEIZUNG+/BAD+/PARTY) (source: modbus/aerosmartm/funktionen.yaml)."""

from __future__ import annotations

from .model import AerosmartComponent, uint32


class BoostFunctionsVentilation(AerosmartComponent):
    """Boost functions (HEIZUNG+/BAD+/PARTY) (ventilation unit registers)."""

    # Funktion HEIZUNG+
    function_heizung_plus = uint32(
        5492,
        writable=True,
        value_kind="boolean",
        source_key="aerosmartm_function_heizung_plus",
        description="Funktion HEIZUNG+",
    )

    # Zeitspanne Funktion HEIZUNG+
    zeitspanne_function_heizung_plus = uint32(
        5494,
        unit="min",
        writable=True,
        source_key="aerosmartm_zeitspanne_function_heizung_plus",
        description="Zeitspanne Funktion HEIZUNG+",
    )

    # Sollwert-Erhöhung Funktion HEIZUNG+
    sollwert_erhoehung_function_heizung_plus = uint32(
        5496,
        unit="K",
        writable=True,
        source_key="aerosmartm_sollwert_erhoehung_function_heizung_plus",
        description="Sollwert-Erhöhung Funktion HEIZUNG+",
    )

    # Zeitspanne Funktion PARTY
    zeitspanne_function_party = uint32(
        5038,
        unit="min",
        writable=True,
        source_key="aerosmartm_zeitspanne_function_party",
        description="Zeitspanne Funktion PARTY",
    )


class BoostFunctionsHeatPump(AerosmartComponent):
    """Boost functions (HEIZUNG+/BAD+/PARTY) (heat pump unit registers)."""

    # Funktion BAD+
    function_bad_plus = uint32(
        5036,
        writable=True,
        value_kind="boolean",
        source_key="aerosmartm_function_bad_plus",
        description="Funktion BAD+",
    )
