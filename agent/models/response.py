"""Response data models."""

from dataclasses import dataclass
from typing import Any


@dataclass
class Response:
    """Represents a response from the agent."""

    success: bool
    data: Any | None = None
    error: str | None = None
    metadata: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert response to dictionary."""
        return {
            "success": self.success,
            "data": self.data,
            "error": self.error,
            "metadata": self.metadata or {}
        }
