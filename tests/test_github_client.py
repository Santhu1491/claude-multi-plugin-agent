from agent.integrations.github_client import GitHubClient


def test_github_client_requires_token(monkeypatch):
    monkeypatch.delenv(
        "GITHUB_TOKEN",
        raising=False,
    )

    try:
        GitHubClient(
            owner="test-owner",
            repo="test-repo",
        )
        assert False
    except ValueError as exc:
        assert "GITHUB_TOKEN" in str(exc)


def test_github_client_uses_explicit_token():
    client = GitHubClient(
        owner="test-owner",
        repo="test-repo",
        token="fake-token",
    )

    assert client.owner == "test-owner"
    assert client.repo == "test-repo"
    assert client.token == "fake-token"

class FakeResponse:
    status_code = 201

    def json(self):
        return {
            "number": 42,
            "html_url": "https://github.com/test-owner/test-repo/pull/42",
        }

    @property
    def text(self):
        return ""


def test_create_pull_request(monkeypatch):
    captured = {}

    def fake_post(url, headers, json, timeout):
        captured["url"] = url
        captured["headers"] = headers
        captured["json"] = json
        captured["timeout"] = timeout

        return FakeResponse()

    monkeypatch.setattr(
        "agent.integrations.github_client.requests.post",
        fake_post,
    )

    client = GitHubClient(
        owner="test-owner",
        repo="test-repo",
        token="fake-token",
    )

    result = client.create_pull_request(
        title="Add feature",
        head="feature/test",
        base="main",
        body="Test PR",
    )

    assert result["number"] == 42
    assert "pull/42" in result["html_url"]

    assert captured["json"]["title"] == "Add feature"
    assert captured["json"]["head"] == "feature/test"
    assert captured["json"]["base"] == "main"

class FailedResponse:
    status_code = 422

    @property
    def text(self):
        return "Validation failed"

    def json(self):
        return {}


def test_create_pull_request_failure(monkeypatch):
    def fake_post(url, headers, json, timeout):
        return FailedResponse()

    monkeypatch.setattr(
        "agent.integrations.github_client.requests.post",
        fake_post,
    )

    client = GitHubClient(
        owner="test-owner",
        repo="test-repo",
        token="fake-token",
    )

    try:
        client.create_pull_request(
            title="Bad PR",
            head="feature/test",
        )
        assert False
    except RuntimeError as exc:
        assert "422" in str(exc)
        assert "Validation failed" in str(exc)