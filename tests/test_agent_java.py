from agent.config.settings import Settings
from agent.core.agent import Agent


def test_agent_uses_java_plugin():
    settings = Settings()
    agent = Agent(settings)

    request = {
        "content": "Create a Java Spring Boot REST API for customer registration"
    }

    result = agent.process_request(request)

    print("\nAgent result:")
    print(result)

    assert result["claude_analysis"]
    assert result["plugin"] == "java"

    assert "success" in result
    assert result["success"] is True