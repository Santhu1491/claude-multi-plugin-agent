"""Main entry point for the multi-plugin agent."""

from agent.core.agent import Agent
from agent.config.settings import Settings


def main() -> None:
    """Initialize and run the agent."""
    settings = Settings()
    agent = Agent(settings)
    print(f"Multi-plugin agent ready (version {settings.version})")
    # agent.run()


if __name__ == "__main__":
    main()
