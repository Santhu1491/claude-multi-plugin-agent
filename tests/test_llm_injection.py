from agent.config.settings import Settings
from agent.core.agent import Agent
from tests.fakes.fake_llm import FakeLLM


def test_agent_accepts_injected_llm():
    settings = Settings()
    fake_llm = FakeLLM()

    agent = Agent(
        settings,
        claude=fake_llm,
    )

    assert agent.claude is fake_llm
    assert agent.file_selector.claude is fake_llm