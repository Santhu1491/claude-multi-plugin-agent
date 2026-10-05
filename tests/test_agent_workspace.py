from agent.config.settings import Settings
from agent.core.agent import Agent
from tests.fakes.fake_llm import FakeLLM


def test_agent_accepts_workspace_root(tmp_path):
    settings = Settings()
    fake_llm = FakeLLM()

    agent = Agent(
        settings,
        claude=fake_llm,
        workspace_root=str(tmp_path),
    )

    assert agent.workspace_root == str(tmp_path)