from agent.config.settings import Settings
from agent.core.agent import Agent
from tests.fakes.fake_llm import FakeLLM


def test_agent_uses_injected_llm():
    settings = Settings()
    fake_llm = FakeLLM()

    agent = Agent(
        settings,
        claude=fake_llm,
    )

    response = agent._analyze_with_claude(
        {"message": "Analyze a Python change"},
        "Repository context",
    )

    assert response
    assert fake_llm.prompts