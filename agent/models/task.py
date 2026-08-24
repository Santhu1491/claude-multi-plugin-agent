"""Task data models."""

from dataclasses import dataclass
from typing import Any


@dataclass
class Task:
    """Represents an executable task for a plugin."""

    plugin: str
    operation: str
    parameters: dict[str, Any]
    priority: int = 1
    dependencies: list[str] | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert task to dictionary."""
        return {
            "plugin": self.plugin,
            "operation": self.operation,
            "parameters": self.parameters,
            "priority": self.priority,
            "dependencies": self.dependencies or []
        }
