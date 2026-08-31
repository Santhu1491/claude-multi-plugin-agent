from agent.core.agent import Agent
from agent.config.settings import Settings


def test_agent_uses_claude():
    settings = Settings()
    agent = Agent(settings)

    request = {
    "message": (
        "Update the existing Python plugin so that it can support "
        "a new operation called validate. Identify which existing "
        "repository files should be modified."
    )
    }

    result = agent.process_request(request)

    print("\nAgent result:")
    print(result)

    assert "claude_analysis" in result
    assert result["claude_analysis"]