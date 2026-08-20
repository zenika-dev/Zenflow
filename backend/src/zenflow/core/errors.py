"""Domain-level errors raised by the Zenflow core, independent of any UI layer."""

from __future__ import annotations


class ZenflowError(Exception):
    """Raised when initialization input or environment is invalid."""
