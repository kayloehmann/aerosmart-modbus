# aerosmart-modbus

A typed, async Python model of an aerosmart ventilation/heat-pump unit's
Modbus registers. Backend-neutral: built on
[modbus-connection](https://pypi.org/project/modbus-connection/), so it runs
over pymodbus, tmodbus, or an in-memory mock -- no Home Assistant dependency.
A Home Assistant integration that consumes this library lives in a separate
repository.

## Features

- 137 registers across 16 sub-systems, transcribed 1:1 from a live
  installation's Modbus register map (address, scale, unit).
- Two Modbus units modelled as one device: unit 1 (ventilation controller,
  which also aggregates most fault/request flags) and unit 2 (heat pump /
  domestic hot water), read together via one `AerosmartDevice` object.
- Neutral per-field metadata (`value_kind`, `writable`, `description`,
  `source_key`) -- no Home Assistant concepts leak into this layer.
- Pooled block reads per unit (`ComponentGroup`), not one Modbus round-trip
  per register.
- A regression test that re-parses the original source YAML and checks every
  Python field's address/scale still matches it (see "Development", below --
  there is no manufacturer register manual to check against instead).

## Device structure

| Attribute | Unit | Sub-system |
|---|---|---|
| `general` | ventilation | weekday, time/date, software version, device type |
| `outside_temperature` | ventilation | outside air temperature + thresholds |
| `room_temperature` | ventilation | room air temperature + setpoint |
| `fans` | ventilation | fan speeds, run hours, faults |
| `ventilation` | ventilation | operating mode, airflow, shading/frost/de-icing |
| `cooling` | ventilation | cooling thresholds |
| `summer_bypass` | ventilation | summer bypass automation |
| `carbon_dioxide` | ventilation | CO2 sensor |
| `fine_dust_filter` / `coarse_dust_filter` | ventilation | filter run time / change flags |
| `fire_alarm` | ventilation | fire alarm system contact |
| `aggregate_fault` | ventilation | summary fault flags |
| `boost_functions_ventilation` | ventilation | HEIZUNG+ boost function (ventilation-side registers) |
| `hot_water_ventilation` | ventilation | hot water fault/request flags (as seen from the controller) |
| `utility_lockout` | heat pump | utility (EVU) lockout signals |
| `heat_pump` | heat pump | compressor, pressures, run hours, status |
| `boost_functions_heat_pump` | heat pump | BAD+ boost function (heat-pump-side registers) |
| `hot_water_heat_pump` | heat pump | boiler temperatures, hot water setpoint |

## Basic usage

```python
import asyncio
from modbus_connection.pymodbus import connect_tcp
from aerosmart_modbus import AerosmartDevice

async def main():
    connection = await connect_tcp("192.0.2.10", port=8899)
    device = AerosmartDevice(
        connection.for_unit(1),  # ventilation
        connection.for_unit(2),  # heat pump
    )
    await device.async_update()
    print(device.outside_temperature.temp_aussenluft, "°C outside")
    print(device.heat_pump.wp_status)

asyncio.run(main())
```

## Known hardware quirk: request pacing

Live-tested against a real unit: this device sits behind a slow
RS232-to-Modbus-TCP gateway. Issuing requests back-to-back with no pacing at
all made the gateway return responses under stale/mismatched transaction IDs,
and most reads timed out. Setting `unit.set_message_spacing(0.3)` (300ms
between requests) on both units, plus a short (~1-2s) settle delay after
connecting and after switching which unit you address, fixed this completely
-- all 137 registers then read cleanly. This library does not set spacing
itself (it only models registers, not connection policy); a consumer talking
to the real gateway should configure it on the `ModbusUnit` it passes in. The
Home Assistant integrations in the sibling repos do this already.

## Metadata and writes

Every field carries a `DatapointMetadata` (see `metadata.py`):
`value_kind` (`"number"` or `"boolean"`), `writable`, `description` (the
original German label), `source_key` (the original Home Assistant entity id
it was transcribed from, for traceability), and either `NumberMetadata` or
`BooleanMetadata`.

```python
meta = device.hot_water_heat_pump.require_metadata_for("wp_brauchwasser_soll_temp")
meta.writable        # True
meta.source_key       # "aerosmartm_wp_brauchwasser_soll_temp"

await device.hot_water_heat_pump.write("wp_brauchwasser_soll_temp", 52.0)
```

**Caution:** `writable=True` here reflects a naming heuristic against an
unverified register map, not a confirmed manufacturer specification -- treat
every writable field as unverified until checked against the real unit.

## Command-line query tool

```bash
python -m pip install -e ".[cli]"
python script/query.py tcp 192.0.2.10 --port 8899
```

Prints every sub-system's current values, plus how many Modbus reads it took.
Not used by CI -- a manual diagnostic tool for probing a real unit.

## Development

```bash
uv sync
uv run pytest
uv run ruff check .
uv run ruff format .
```

Tests run against `modbus_connection`'s in-memory mock (no real device
needed) plus a YAML consistency check (`tests/test_yaml_consistency.py`)
against the original source fragments under `tests/fixtures/aerosmartm/`.
Tested against `modbus-connection` 3.4.x.
