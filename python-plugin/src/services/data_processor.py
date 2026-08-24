"""Data processing service."""

from collections.abc import Iterable
from typing import Any


def process_records(records: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return a materialized list of input records."""
    return list(records)
