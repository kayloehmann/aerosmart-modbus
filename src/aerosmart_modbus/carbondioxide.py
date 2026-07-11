"""CO2 sensor (source: modbus/aerosmartm/carbondioxide.yaml)."""

from __future__ import annotations

from .model import AerosmartComponent, uint32


class CarbonDioxide(AerosmartComponent):
    """CO2 sensor."""

    # CO2-Messung
    co2_measurement = uint32(
        1048, source_key="aerosmartm_co2_measurement", description="CO2-Messung"
    )

    # CO2-Sensor vorhanden?
    co2_sensor_available = uint32(
        5054,
        value_kind="boolean",
        source_key="aerosmartm_co2_sensor_available",
        description="CO2-Sensor vorhanden?",
    )

    # Störung: CO2 Sensor
    stoerung_co2_sensor = uint32(
        832,
        value_kind="boolean",
        source_key="aerosmartm_stoerung_co2_sensor",
        description="Störung: CO2 Sensor",
    )

    # CO2
    co2 = uint32(230, unit="ppm", source_key="aerosmartm_co2", description="CO2")
