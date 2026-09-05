from agent.integrations.azure_devops_client import (
    AzureDevOpsClient,
)


def test_client_uses_explicit_configuration():
    client = AzureDevOpsClient(
        organization="test-org",
        project="test-project",
        pat="fake-pat",
    )

    assert client.organization == "test-org"
    assert client.project == "test-project"
    assert client.pat == "fake-pat"

    assert client.base_url == (
        "https://dev.azure.com/"
        "test-org/test-project"
    )


def test_client_requires_organization(monkeypatch):
    monkeypatch.delenv(
        "AZURE_DEVOPS_ORG",
        raising=False,
    )

    try:
        AzureDevOpsClient(
            project="test-project",
            pat="fake-pat",
        )
        assert False
    except ValueError as exc:
        assert "AZURE_DEVOPS_ORG" in str(exc)


def test_client_requires_project(monkeypatch):
    monkeypatch.delenv(
        "AZURE_DEVOPS_PROJECT",
        raising=False,
    )

    try:
        AzureDevOpsClient(
            organization="test-org",
            pat="fake-pat",
        )
        assert False
    except ValueError as exc:
        assert "AZURE_DEVOPS_PROJECT" in str(exc)


def test_client_requires_pat(monkeypatch):
    monkeypatch.delenv(
        "AZURE_DEVOPS_PAT",
        raising=False,
    )

    try:
        AzureDevOpsClient(
            organization="test-org",
            project="test-project",
        )
        assert False
    except ValueError as exc:
        assert "AZURE_DEVOPS_PAT" in str(exc)

class FakeResponse:
    status_code = 200

    def json(self):
        return {
            "id": 123,
            "fields": {
                "System.Title": "Add validation support",
            },
        }

    @property
    def text(self):
        return ""


def test_get_work_item(monkeypatch):
    def fake_get(
        url,
        auth,
        headers,
        timeout,
    ):
        assert "_apis/wit/workitems/123" in url
        assert auth == ("", "fake-pat")

        return FakeResponse()

    monkeypatch.setattr(
        "agent.integrations.azure_devops_client.requests.get",
        fake_get,
    )

    client = AzureDevOpsClient(
        organization="test-org",
        project="test-project",
        pat="fake-pat",
    )

    item = client.get_work_item(123)

    assert item["id"] == 123
    assert (
        item["fields"]["System.Title"]
        == "Add validation support"
    )

class FakePRResponse:
    status_code = 201

    def json(self):
        return {
            "pullRequestId": 42,
            "title": "Test PR",
        }

    @property
    def text(self):
        return ""


def test_create_pull_request(monkeypatch):
    captured = {}

    def fake_post(
        url,
        auth,
        headers,
        json,
        timeout,
    ):
        captured["url"] = url
        captured["json"] = json

        return FakePRResponse()

    monkeypatch.setattr(
        "agent.integrations.azure_devops_client.requests.post",
        fake_post,
    )

    client = AzureDevOpsClient(
        organization="test-org",
        project="test-project",
        pat="fake-pat",
    )

    result = client.create_pull_request(
        repository_id="repo-123",
        source_branch="feature/work-item-123",
        target_branch="main",
        title="Implement work item 123",
        description="Automated PR",
    )

    assert result["pullRequestId"] == 42

    assert captured["json"]["sourceRefName"] == (
        "refs/heads/feature/work-item-123"
    )

    assert captured["json"]["targetRefName"] == (
        "refs/heads/main"
    )

class FakeUpdateResponse:
    status_code = 200

    def json(self):
        return {
            "id": 123,
            "rev": 5,
        }

    @property
    def text(self):
        return ""


def test_update_work_item(monkeypatch):
    captured = {}

    def fake_patch(
        url,
        auth,
        headers,
        json,
        timeout,
    ):
        captured["url"] = url
        captured["json"] = json
        captured["headers"] = headers

        return FakeUpdateResponse()

    monkeypatch.setattr(
        "agent.integrations.azure_devops_client.requests.patch",
        fake_patch,
    )

    client = AzureDevOpsClient(
        organization="test-org",
        project="test-project",
        pat="fake-pat",
    )

    result = client.update_work_item(
        work_item_id=123,
        fields={
            "System.History": (
                "Automated PR created successfully."
            )
        },
    )

    assert result["id"] == 123

    assert captured["json"] == [
        {
            "op": "add",
            "path": "/fields/System.History",
            "value": (
                "Automated PR created successfully."
            ),
        }
    ]

    assert (
        captured["headers"]["Content-Type"]
        == "application/json-patch+json"
    )