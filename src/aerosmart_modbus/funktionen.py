"""Boost functions (HEIZUNG+/BAD+/PARTY) (source: modbus/aerosmartm/funktionen.yaml)."""

from __future__ import annotations

from .model import AerosmartComponent, uint32


class BoostFunctionsVentilation(AerosmartComponent):
    """Boost functions (HEIZUNG+/BAD+/PARTY) (ventilation unit registers)."""

    # Funktion HEIZUNG+
    # Verified against official Drexel & Weiss Modbus documentation
    # (aerosmart_m_modbus.pdf, "Modbus_Parameter_aerosmart_m", p.55-63): R/W, 0/1.
    function_heizung_plus = uint32(
        5492,
        writable=True,
        value_kind="boolean",
        source_key="aerosmartm_function_heizung_plus",
        description="Funktion HEIZUNG+",
    )

    # Zeitspanne Funktion HEIZUNG+
    # Official doc: R/W, raw 1800-14400 = 30-240 min -> the register stores
    # seconds despite the source YAML's "min" unit label; scale=1/60 corrects
    # both the display value and the value this integration would write.
    zeitspanne_function_heizung_plus = uint32(
        5494,
        scale=0.0166666667,
        unit="min",
        writable=True,
        min_value=30,
        max_value=240,
        source_key="aerosmartm_zeitspanne_function_heizung_plus",
        description="Zeitspanne Funktion HEIZUNG+",
    )

    # Sollwert-Erhöhung Funktion HEIZUNG+
    # Official doc: R/W, raw 300-2000 = 0.3-2.0 K -> scale=0.001 (missing
    # entirely before; the source YAML carried no scale for this register).
    sollwert_erhoehung_function_heizung_plus = uint32(
        5496,
        scale=0.001,
        unit="K",
        writable=True,
        min_value=0.3,
        max_value=2.0,
        source_key="aerosmartm_sollwert_erhoehung_function_heizung_plus",
        description="Sollwert-Erhöhung Funktion HEIZUNG+",
    )

    # Zeitspanne Funktion PARTY
    # Official doc gives R/W, 60-240 min but no explicit raw range for this
    # specific register; scale=1/60 applied by analogy to the structurally
    # identical "Zeitspanne Funktion HEIZUNG+" (5494) above -- unconfirmed for
    # this exact address, verify by reading back before relying on it.
    zeitspanne_function_party = uint32(
        5038,
        scale=0.0166666667,
        unit="min",
        writable=True,
        min_value=60,
        max_value=240,
        source_key="aerosmartm_zeitspanne_function_party",
        description="Zeitspanne Funktion PARTY",
    )


class BoostFunctionsHeatPump(AerosmartComponent):
    """Boost functions (HEIZUNG+/BAD+/PARTY) (heat pump unit registers)."""

    # Funktion BAD+
    # Official doc: R/W, 0/1 -- but only listed in the WP (heat pump) register
    # table, not the LU (ventilation-only) table; may not exist on installations
    # without a heat pump.
    function_bad_plus = uint32(
        5036,
        writable=True,
        value_kind="boolean",
        source_key="aerosmartm_function_bad_plus",
        description="Funktion BAD+",
    )
