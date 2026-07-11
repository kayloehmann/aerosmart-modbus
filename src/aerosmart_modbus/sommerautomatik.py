"""Summer bypass automation (source: modbus/aerosmartm/sommerautomatik.yaml)."""

from __future__ import annotations

from .model import AerosmartComponent, uint32


class SummerBypass(AerosmartComponent):
    """Summer bypass automation."""

    # Betriebsart Sommerautomatik
    betriebsart_sommerautomatik = uint32(
        1300,
        source_key="aerosmartm_betriebsart_sommerautomatik",
        description="Betriebsart Sommerautomatik",
    )

    # Anforderung: Sommerautomatik (read)
    anforderung_sommerautomatik = uint32(
        1322,
        value_kind="boolean",
        source_key="aerosmartm_anforderung_sommerautomatik",
        description="Anforderung: Sommerautomatik (read)",
    )

    # Funktion „Sommerautomatik“
    function_sommerautomatik = uint32(
        5384,
        writable=True,
        value_kind="boolean",
        source_key="aerosmartm_function_sommerautomatik",
        description="Funktion „Sommerautomatik“",
    )

    # Sommerautomatik Schaltpunkt 1
    sommerautomatik_schaltpunkt1 = uint32(
        5390,
        writable=True,
        source_key="aerosmartm_sommerautomatik_schaltpunkt1",
        description="Sommerautomatik Schaltpunkt 1",
    )

    # Sommerautomatik Schaltpunkt 2
    sommerautomatik_schaltpunkt2 = uint32(
        5392,
        writable=True,
        source_key="aerosmartm_sommerautomatik_schaltpunkt2",
        description="Sommerautomatik Schaltpunkt 2",
    )

    # Sommerautomatik Schaltpunkt 3
    sommerautomatik_schaltpunkt3 = uint32(
        5394,
        writable=True,
        source_key="aerosmartm_sommerautomatik_schaltpunkt3",
        description="Sommerautomatik Schaltpunkt 3",
    )

    # Sommerautomatik Schaltpunkt 4
    sommerautomatik_schaltpunkt4 = uint32(
        5396,
        writable=True,
        source_key="aerosmartm_sommerautomatik_schaltpunkt4",
        description="Sommerautomatik Schaltpunkt 4",
    )
