"""Conversation and execution context management."""

from datetime import datetime, timezone
from typing import Any


class Context:
    """Maintains conversation history and execution state."""

    def __init__(self) -> None:
        self.messages: list[dict[str, Any]] = []
        self.state: dict[str, Any] = {}
        self.metadata: dict[str, Any] = {
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        }

    def add_message(self, message: dict[str, Any]) -> None:
        """Add a message to the conversation history."""
        self.messages.append({
            **message,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
        self.metadata["updated_at"] = datetime.now(timezone.utc).isoformat()

    def get_history(self, limit: int = 10) -> list[dict[str, Any]]:
        """Retrieve recent conversation history."""
        return self.messages[-limit:]

    def set_state(self, key: str, value: Any) -> None:
        """Set a state variable."""
        self.state[key] = value
        self.metadata["updated_at"] = datetime.now(timezone.utc).isoformat()

    def get_state(self, key: str, default: Any = None) -> Any:
        """Retrieve a state variable."""
        return self.state.get(key, default)

    def clear(self) -> None:
        """Clear context history and state."""
        self.messages.clear()
        self.state.clear()
        self.metadata["updated_at"] = datetime.now(timezone.utc).isoformat()
