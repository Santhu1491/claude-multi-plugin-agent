"""Main entry point for the multi-plugin agent."""

from agent.config.settings import Settings
from agent.core.agent import Agent


def main() -> None:
    """Initialize and run the agent."""
    settings = Settings()
    Agent(settings)
    print(f"Multi-plugin agent ready (version {settings.version})")
    # agent.run()


if __name__ == "__main__":
    main()
