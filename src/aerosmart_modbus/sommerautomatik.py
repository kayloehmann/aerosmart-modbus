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
    # CORRECTED against official Drexel & Weiss documentation: this is
    # read-only (a status readback, 0/1), not a writable boost switch --
    # the "Funktion X" naming pattern that flagged the other two boost
    # functions as writable does not hold here. Verify before assuming this
    # or any other field's writability from naming alone.
    function_sommerautomatik = uint32(
        5384,
        value_kind="boolean",
        source_key="aerosmartm_function_sommerautomatik",
        description="Funktion „Sommerautomatik“ (Status, nicht schaltbar)",
    )

    # Sommerautomatik Schaltpunkt 1
    # Official doc confirms R/W and a raw range of 0-2400, but leaves the
    # unit column blank -- unconfirmed. 0-2400 matches the shape of an HHMM
    # time encoding (vs. "Uhrzeit" 5212's 0-235959 HHMMSS), but that is an
    # analogy, not a documented fact. Do not write without verifying by
    # reading back a known value first.
    sommerautomatik_schaltpunkt1 = uint32(
        5390,
        writable=True,
        min_value=0,
        max_value=2400,
        source_key="aerosmartm_sommerautomatik_schaltpunkt1",
        description="Sommerautomatik Schaltpunkt 1",
    )

    # Sommerautomatik Schaltpunkt 2 (see schaltpunkt1 note on unit/range)
    sommerautomatik_schaltpunkt2 = uint32(
        5392,
        writable=True,
        min_value=0,
        max_value=2400,
        source_key="aerosmartm_sommerautomatik_schaltpunkt2",
        description="Sommerautomatik Schaltpunkt 2",
    )

    # Sommerautomatik Schaltpunkt 3 (see schaltpunkt1 note on unit/range)
    sommerautomatik_schaltpunkt3 = uint32(
        5394,
        writable=True,
        min_value=0,
        max_value=2400,
        source_key="aerosmartm_sommerautomatik_schaltpunkt3",
        description="Sommerautomatik Schaltpunkt 3",
    )

    # Sommerautomatik Schaltpunkt 4 (see schaltpunkt1 note on unit/range)
    sommerautomatik_schaltpunkt4 = uint32(
        5396,
        writable=True,
        min_value=0,
        max_value=2400,
        source_key="aerosmartm_sommerautomatik_schaltpunkt4",
        description="Sommerautomatik Schaltpunkt 4",
    )
