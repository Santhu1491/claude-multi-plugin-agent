"""Data models used by the Python plugin."""

from dataclasses import dataclass
from typing import Any


@dataclass
class PluginRequest:
    """A request sent to a plugin service."""

    operation: str
    payload: dict[str, Any]


@dataclass
class PluginResponse:
    """A response returned by a plugin service."""

    success: bool
    result: Any
