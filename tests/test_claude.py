import pytest

from agent.integrations.claude import ClaudeClient

pytestmark = pytest.mark.live_claude


def test_claude_connection():
    client = ClaudeClient()

    response = client.generate(
        "Respond with exactly: Claude connection successful."
    )

    print("\nClaude response:", response)

    assert response