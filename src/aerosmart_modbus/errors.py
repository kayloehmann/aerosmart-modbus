"""Exceptions raised by aerosmart-specific safety checks."""

from __future__ import annotations

from typing import Any


class UnverifiedWriteError(ValueError):
    """A write was attempted for a register not verified by documentation."""


class WriteVerificationError(RuntimeError):
    """The controller did not retain the requested value."""

    def __init__(self, component: str, field: str, requested: Any, actual: Any) -> None:
        super().__init__(
            f"write verification failed for {component}.{field}: "
            f"requested {requested!r}, read back {actual!r}"
        )
        self.component = component
        self.field = field
        self.requested = requested
        self.actual = actual
