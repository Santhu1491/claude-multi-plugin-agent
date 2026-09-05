from agent.integrations.jira_client import JiraClient


def test_jira_client_requires_email(monkeypatch):
    monkeypatch.delenv(
        "JIRA_EMAIL",
        raising=False,
    )

    monkeypatch.delenv(
        "JIRA_API_TOKEN",
        raising=False,
    )

    try:
        JiraClient(
            base_url="https://example.atlassian.net",
            api_token="fake-token",
        )
        assert False
    except ValueError as exc:
        assert "JIRA_EMAIL" in str(exc)


def test_jira_client_requires_token(monkeypatch):
    monkeypatch.delenv(
        "JIRA_API_TOKEN",
        raising=False,
    )

    try:
        JiraClient(
            base_url="https://example.atlassian.net",
            email="test@example.com",
        )
        assert False
    except ValueError as exc:
        assert "JIRA_API_TOKEN" in str(exc)


def test_jira_client_explicit_credentials():
    client = JiraClient(
        base_url="https://example.atlassian.net/",
        email="test@example.com",
        api_token="fake-token",
    )

    assert client.base_url == "https://example.atlassian.net"
    assert client.email == "test@example.com"
    assert client.api_token == "fake-token"

class FakeResponse:
    status_code = 200

    def json(self):
        return {
            "key": "PROJ-123",
            "fields": {
                "summary": "Add validation support",
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {
                                    "type": "text",
                                    "text": "Add validation support to the Python plugin.",
                                }
                            ],
                        }
                    ],
                },
                "labels": [
                    "tech:python",
                    "backend",
                ],
            },
        }

    @property
    def text(self):
        return ""


def test_jira_get_issue(monkeypatch):
    def fake_get(url, auth, headers, timeout):
        return FakeResponse()

    monkeypatch.setattr(
        "agent.integrations.jira_client.requests.get",
        fake_get,
    )

    client = JiraClient(
        base_url="https://example.atlassian.net",
        email="test@example.com",
        api_token="fake-token",
    )

    issue = client.get_issue("PROJ-123")

    assert issue["key"] == "PROJ-123"
    assert issue["fields"]["summary"] == "Add validation support"
    assert "tech:python" in issue["fields"]["labels"]