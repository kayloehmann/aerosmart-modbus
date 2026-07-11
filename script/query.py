#!/usr/bin/env python3
"""Manual CLI query client for an aerosmart unit -- no Home Assistant involved.

Connects over Modbus TCP, reads the whole device once, and prints every
subsystem with its values and units. A development/diagnostic tool, not used
by CI.

Usage:
    python -m pip install -e ".[cli]"
    python script/query.py tcp 192.0.2.10 --port 8899
"""

from __future__ import annotations

import argparse
import asyncio
import sys
import time

from aerosmart_modbus import AerosmartDevice
from aerosmart_modbus.aerosmart import DEFAULT_UNIT_HEAT_PUMP, DEFAULT_UNIT_VENTILATION


class _CountingUnit:
    """Wraps a ModbusUnit to count actual reads, for the summary line."""

    def __init__(self, unit):
        self._unit = unit
        self.reads = 0

    async def read_holding_registers(self, address, count):
        self.reads += 1
        return await self._unit.read_holding_registers(address, count)

    async def read_input_registers(self, address, count):
        self.reads += 1
        return await self._unit.read_input_registers(address, count)

    async def write_register(self, address, value):
        return await self._unit.write_register(address, value)

    async def write_registers(self, address, values):
        return await self._unit.write_registers(address, values)

    async def read_coils(self, address, count):
        self.reads += 1
        return await self._unit.read_coils(address, count)

    async def read_discrete_inputs(self, address, count):
        self.reads += 1
        return await self._unit.read_discrete_inputs(address, count)

    async def write_coil(self, address, value):
        return await self._unit.write_coil(address, value)


def _print_component(title: str, component) -> None:
    print(f"\n=== {title} ===")
    for attr, field in component._register_fields.items():
        meta = getattr(field, "aerosmart_metadata", None)
        value = getattr(component, attr)
        unit = meta.number.unit if meta and meta.number and meta.number.unit else ""
        flag = " [writable]" if meta and meta.writable else ""
        label = meta.description if meta and meta.description else attr
        print(f"  {attr:55s} = {value!r:>12} {unit}{flag}  ({label})")


async def _run(args: argparse.Namespace) -> None:
    if args.transport == "tcp":
        from modbus_connection.pymodbus import connect_tcp

        connection = await connect_tcp(args.host, port=args.port)
    else:
        from modbus_connection.pymodbus import connect_serial

        connection = await connect_serial(args.host, baudrate=args.baudrate)

    unit_v = _CountingUnit(connection.for_unit(args.unit_ventilation))
    unit_h = _CountingUnit(connection.for_unit(args.unit_heat_pump))
    device = AerosmartDevice(unit_v, unit_h)

    start = time.monotonic()
    await device.async_update()
    elapsed_ms = (time.monotonic() - start) * 1000

    _print_component("General", device.general)
    _print_component("Outside temperature", device.outside_temperature)
    _print_component("Room temperature", device.room_temperature)
    _print_component("Fans", device.fans)
    _print_component("Ventilation", device.ventilation)
    _print_component("Cooling", device.cooling)
    _print_component("Summer bypass", device.summer_bypass)
    _print_component("CO2", device.carbon_dioxide)
    _print_component("Fine dust filter", device.fine_dust_filter)
    _print_component("Coarse dust filter", device.coarse_dust_filter)
    _print_component("Fire alarm", device.fire_alarm)
    _print_component("Aggregate fault", device.aggregate_fault)
    _print_component(
        "Boost functions (ventilation)", device.boost_functions_ventilation
    )
    _print_component(
        "Hot water (ventilation-side status)", device.hot_water_ventilation
    )
    _print_component("Utility lockout", device.utility_lockout)
    _print_component("Heat pump", device.heat_pump)
    _print_component("Boost functions (heat pump)", device.boost_functions_heat_pump)
    _print_component("Hot water (heat pump)", device.hot_water_heat_pump)

    reads = unit_v.reads + unit_h.reads
    print(f"\nQueried in {elapsed_ms:.0f}ms ({reads} Modbus reads)")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="transport", required=True)

    tcp = sub.add_parser("tcp", help="Modbus TCP")
    tcp.add_argument("host")
    tcp.add_argument("--port", type=int, default=502)

    serial = sub.add_parser("serial", help="Modbus RTU over a serial port")
    serial.add_argument("host", help="e.g. /dev/ttyUSB0")
    serial.add_argument("--baudrate", type=int, default=9600)

    for sp in (tcp, serial):
        sp.add_argument(
            "--unit-ventilation", type=int, default=DEFAULT_UNIT_VENTILATION
        )
        sp.add_argument("--unit-heat-pump", type=int, default=DEFAULT_UNIT_HEAT_PUMP)

    args = parser.parse_args()
    try:
        asyncio.run(_run(args))
    except KeyboardInterrupt:
        sys.exit(130)


if __name__ == "__main__":
    main()
