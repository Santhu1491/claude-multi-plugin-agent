"""Request data models."""

from dataclasses import dataclass
from typing import Any


@dataclass
class Request:
    """Represents a user request to the agent."""

    content: str
    operation: str | None = None
    parameters: dict[str, Any] | None = None
    context: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert request to dictionary."""
        return {
            "content": self.content,
            "operation": self.operation,
            "parameters": self.parameters or {},
            "context": self.context or {}
        }
