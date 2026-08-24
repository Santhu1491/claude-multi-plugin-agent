"""Application settings and configuration."""

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Settings:
    """Application configuration settings."""

    version: str = "0.1.0"
    api_key: str | None = None
    plugin_directory: Path | None = None
    log_level: str = "INFO"
    max_retries: int = 3
    timeout: int = 30

    def __post_init__(self) -> None:
        """Load settings from environment."""
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        
        if self.plugin_directory is None:
            self.plugin_directory = Path(__file__).parent.parent.parent / "plugins"

    def validate(self) -> bool:
        """Validate configuration."""
        if not self.api_key:
            print("Warning: ANTHROPIC_API_KEY not set")
            return False
        return True
