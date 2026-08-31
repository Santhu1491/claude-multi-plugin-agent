from agent.integrations.claude import ClaudeClient


def test_claude_connection():
    client = ClaudeClient()

    response = client.generate(
        "Respond with exactly: Claude connection successful."
    )

    print("\nClaude response:", response)

    assert response