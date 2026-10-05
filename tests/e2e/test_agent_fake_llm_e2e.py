from pathlib import Path

import pytest

from agent.config.settings import Settings
from agent.core.agent import Agent
from tests.fakes.fake_llm import FakeLLM

pytestmark = pytest.mark.e2e_fake


def test_agent_end_to_end_with_fake_llm(tmp_path):
    repo_root = Path(tmp_path)

    target_dir = repo_root / "agent" / "utils"
    target_dir.mkdir(parents=True)

    (target_dir / "__init__.py").write_text(
        "",
        encoding="utf-8",
    )

    tests_dir = repo_root / "tests"
    tests_dir.mkdir()

    (tests_dir / "test_validation.py").write_text(
        (
            "def test_placeholder():\n"
            "    assert True\n"
        ),
        encoding="utf-8",
    )

    settings = Settings()
    fake_llm = FakeLLM()

    agent = Agent(
        settings,
        claude=fake_llm,
        workspace_root=str(repo_root),
    )

    request = {
        "message": (
            "Create agent/utils/live_validation.py "
            "with a hello_validation function."
        ),
        "technology": "python",
    }

    result = agent.process_request(request)

    generated_file = (
        repo_root
        / "agent"
        / "utils"
        / "live_validation.py"
    )

    assert result["success"] is True
    assert generated_file.exists()

    assert generated_file.read_text(
        encoding="utf-8"
    ) == (
        'def hello_validation() -> str:\n'
        '    return "hello from live validation"\n'
    )