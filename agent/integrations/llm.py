"""Common interface for language model clients."""

from typing import Protocol


class LLMClient(Protocol):
    """Interface implemented by language model clients."""

    def generate(self, prompt: str) -> str:
        """Generate a response for the supplied prompt."""
        ...