import pytest

from agent.core.azure_boards_publisher import AzureBoardsPublisher


class FakeGitClient:
    def __init__(
        self,
        changes: bool = True,
        active_branch: str = "main",
    ):
        self.calls = []
        self.changes = changes
        self.active_branch = active_branch

    def has_changes(self):
        self.calls.append(
            ("has_changes",)
        )
        return self.changes

    def current_branch(self):
        self.calls.append(
            ("current_branch",)
        )
        return self.active_branch

    def create_branch(self, branch_name):
        self.calls.append(
            ("create_branch", branch_name)
        )
        self.active_branch = branch_name

        return branch_name

    def ensure_safe_branch(self):
        self.calls.append(
            ("ensure_safe_branch",)
        )

        if self.active_branch in {
            "main",
            "master",
        }:
            raise RuntimeError(
                "Unsafe branch."
            )

    def commit(self, message):
        self.calls.append(
            ("commit", message)
        )
        return "abc123"

    def push(self, branch_name):
        self.calls.append(
            ("push", branch_name)
        )


class FakeAzureClient:
    def __init__(self):
        self.calls = []
        self.update_calls = []

    def create_pull_request(
        self,
        repository_id,
        source_branch,
        target_branch,
        title,
        description,
    ):
        self.calls.append(
            (
                repository_id,
                source_branch,
                target_branch,
                title,
            )
        )

        return {
            "pullRequestId": 42,
        }

    def update_work_item(
        self,
        work_item_id,
        fields,
    ):
        self.update_calls.append(
            (
                work_item_id,
                fields,
            )
        )

        return {
            "id": work_item_id,
        }


def test_prepare_branch_creates_work_item_branch():
    git_client = FakeGitClient(
        changes=False,
        active_branch="main",
    )

    azure_client = FakeAzureClient()

    publisher = AzureBoardsPublisher(
        git_client=git_client,
        azure_client=azure_client,
        repository_id="repo-123",
    )

    branch = publisher.prepare_branch(
        {
            "work_item_id": 42,
        }
    )

    assert branch == "feature/work-item-42"

    assert git_client.active_branch == (
        "feature/work-item-42"
    )

    assert (
        "create_branch",
        "feature/work-item-42",
    ) in git_client.calls

    assert (
        "ensure_safe_branch",
    ) in git_client.calls


def test_prepare_branch_rejects_dirty_working_tree():
    git_client = FakeGitClient(
        changes=True,
        active_branch="main",
    )

    azure_client = FakeAzureClient()

    publisher = AzureBoardsPublisher(
        git_client=git_client,
        azure_client=azure_client,
        repository_id="repo-123",
    )

    with pytest.raises(
        RuntimeError,
        match="Working tree must be clean",
    ):
        publisher.prepare_branch(
            {
                "work_item_id": 42,
            }
        )


def test_prepare_branch_requires_base_branch():
    git_client = FakeGitClient(
        changes=False,
        active_branch="feature/old-work",
    )

    azure_client = FakeAzureClient()

    publisher = AzureBoardsPublisher(
        git_client=git_client,
        azure_client=azure_client,
        repository_id="repo-123",
    )

    with pytest.raises(
        RuntimeError,
        match="must start from",
    ):
        publisher.prepare_branch(
            {
                "work_item_id": 42,
            }
        )


def test_azure_boards_publisher():
    git_client = FakeGitClient(
        changes=True,
        active_branch="feature/work-item-123",
    )

    azure_client = FakeAzureClient()

    publisher = AzureBoardsPublisher(
        git_client=git_client,
        azure_client=azure_client,
        repository_id="repo-123",
    )

    result = publisher.publish(
        request={
            "work_item_id": 123,
            "technology": "python",
            "message": "Implement work item 123",
        },
        agent_result={
            "success": True,
        },
    )

    assert result["branch"] == (
        "feature/work-item-123"
    )

    assert result["commit"] == "abc123"
    assert result["pr_id"] == 42

    assert (
        "commit",
        "feat: implement work item 123",
    ) in git_client.calls

    assert (
        "push",
        "feature/work-item-123",
    ) in git_client.calls

    assert azure_client.calls == [
        (
            "repo-123",
            "feature/work-item-123",
            "main",
            "Implement work item 123",
        )
    ]

    assert len(
        azure_client.update_calls
    ) == 1

    updated_work_item_id, fields = (
        azure_client.update_calls[0]
    )

    assert updated_work_item_id == 123
    assert "System.History" in fields
    assert "PR 42" in fields[
        "System.History"
    ]


def test_azure_boards_publisher_rejects_no_changes():
    git_client = FakeGitClient(
        changes=False,
        active_branch="feature/work-item-123",
    )

    azure_client = FakeAzureClient()

    publisher = AzureBoardsPublisher(
        git_client=git_client,
        azure_client=azure_client,
        repository_id="repo-123",
    )

    with pytest.raises(
        RuntimeError,
        match="No repository changes",
    ):
        publisher.publish(
            request={
                "work_item_id": 123,
                "technology": "python",
                "message": "Implement work item 123",
            },
            agent_result={
                "success": True,
            },
        )

    assert azure_client.calls == []
    assert azure_client.update_calls == []


def test_azure_boards_publisher_rejects_failed_agent_result():
    git_client = FakeGitClient(
        changes=True,
        active_branch="feature/work-item-123",
    )

    azure_client = FakeAzureClient()

    publisher = AzureBoardsPublisher(
        git_client=git_client,
        azure_client=azure_client,
        repository_id="repo-123",
    )

    with pytest.raises(
        RuntimeError,
        match="Agent execution failed",
    ):
        publisher.publish(
            request={
                "work_item_id": 123,
                "technology": "python",
                "message": "Implement work item 123",
            },
            agent_result={
                "success": False,
            },
        )

    assert git_client.calls == []
    assert azure_client.calls == []
    assert azure_client.update_calls == []


def test_azure_boards_publisher_rejects_wrong_active_branch():
    git_client = FakeGitClient(
        changes=True,
        active_branch="main",
    )

    azure_client = FakeAzureClient()

    publisher = AzureBoardsPublisher(
        git_client=git_client,
        azure_client=azure_client,
        repository_id="repo-123",
    )

    with pytest.raises(
        RuntimeError,
        match="Expected active branch",
    ):
        publisher.publish(
            request={
                "work_item_id": 123,
                "technology": "python",
                "message": "Implement work item 123",
            },
            agent_result={
                "success": True,
            },
        )

    assert azure_client.calls == []