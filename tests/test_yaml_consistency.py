"""Regression guard: every Python field matches its source YAML 1:1.

Check register addresses and scales against the original Home Assistant
Modbus YAML, with exceptions for scales verified against the manufacturer
register table.
"""

from __future__ import annotations

import re
from pathlib import Path

from aerosmart_modbus import aerosmart

FIXTURES = Path(__file__).parent / "fixtures" / "aerosmartm"

FIELD_RE = re.compile(r"^(name|slave|address|input_type|data_type|scale):\s*(.*?)\s*$")

# Fields whose scale was corrected against the official Drexel & Weiss Modbus
# documentation (aerosmart_m_modbus.pdf, "Modbus_Parameter_aerosmart_m",
# p.55-63) after it was found to differ from the source YAML's missing or
# incorrect scale. Page 60 lists a divisor of 60 for registers 910 and 916–922
# (916, 918, 920, 922).
VERIFIED_SCALE_OVERRIDES = {
    "aerosmartm_zeitspanne_function_heizung_plus": 0.0166666667,
    "aerosmartm_sollwert_erhoehung_function_heizung_plus": 0.001,
    "aerosmartm_zeitspanne_function_party": 0.0166666667,
    "aerosmartm_wp_verdamperregister": 0.01,
    "aerosmartm_wp_betriebsstunden_kompressormotor": 1 / 60,
    "aerosmartm_wp_betriebsstunden_magnetventil_fluessiggas": 1 / 60,
    "aerosmartm_wp_betriebsstunden_magnetventil_heissgas": 1 / 60,
    "aerosmartm_wp_betriebsstunden_magnetventil_luftkondensator": 1 / 60,
    "aerosmartm_wp_betriebsstunden_elektroheizstab": 1 / 60,
}


def _parse_yaml_fixtures() -> dict[str, dict[str, str]]:
    """source_key -> {slave, address, data_type, scale} across all fixtures."""
    by_name: dict[str, dict[str, str]] = {}
    for path in FIXTURES.glob("*.yaml"):
        text = path.read_text(encoding="utf-8")
        blocks = re.split(r"(?=^\s*-\s*name:\s*\S)", text, flags=re.MULTILINE)
        for block in blocks:
            if "name:" not in block:
                continue
            entry: dict[str, str] = {}
            for raw_line in block.splitlines():
                line = raw_line.strip().lstrip("-").strip()
                m = FIELD_RE.match(line)
                if m:
                    entry[m.group(1)] = m.group(2).strip().strip('"')
            if "name" in entry:
                by_name[entry["name"]] = entry
    return by_name


def _all_components() -> list[aerosmart.AerosmartComponent]:
    """Every distinct AerosmartComponent subclass instance across the device.

    Constructed against throwaway unit stand-ins -- only class-level field
    metadata is inspected, no I/O happens.
    """
    from modbus_connection.mock import MockModbusConnection

    conn = MockModbusConnection()
    device = aerosmart.AerosmartDevice(conn.for_unit(1), conn.for_unit(2))
    return [
        device.general,
        device.outside_temperature,
        device.fire_alarm,
        device.carbon_dioxide,
        device.fine_dust_filter,
        device.coarse_dust_filter,
        device.cooling,
        device.ventilation,
        device.room_temperature,
        device.summer_bypass,
        device.aggregate_fault,
        device.fans,
        device.boost_functions_ventilation,
        device.hot_water_ventilation,
        device.utility_lockout,
        device.heat_pump,
        device.boost_functions_heat_pump,
        device.hot_water_heat_pump,
    ]


def test_every_python_field_matches_its_source_yaml():
    yaml_by_name = _parse_yaml_fixtures()
    checked = 0

    for component in _all_components():
        for attr, field in component._register_fields.items():
            meta = getattr(field, "aerosmart_metadata", None)
            assert meta is not None, (
                f"{type(component).__name__}.{attr} has no metadata"
            )
            assert meta.source_key is not None
            yaml_entry = yaml_by_name.get(meta.source_key)
            assert yaml_entry is not None, (
                f"{meta.source_key} (Python attr {attr}) not found in YAML fixtures"
            )
            assert field.address == int(yaml_entry["address"]), meta.source_key
            expected_scale = VERIFIED_SCALE_OVERRIDES.get(
                meta.source_key, float(yaml_entry.get("scale", "1") or "1")
            )
            assert field.scale == expected_scale, meta.source_key
            checked += 1

    assert checked == len(yaml_by_name), (
        f"checked {checked} fields but YAML fixtures declare {len(yaml_by_name)} -- "
        "a register was dropped or duplicated during transcription"
    )
