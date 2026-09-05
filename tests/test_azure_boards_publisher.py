from agent.core.azure_boards_publisher import (
    AzureBoardsPublisher,
)


class FakeGitClient:
    def __init__(self):
        self.calls = []

    def create_branch(self, branch_name):
        self.calls.append(
            ("create_branch", branch_name)
        )

    def stage_all(self):
        self.calls.append(
            ("stage_all",)
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


def test_azure_boards_publisher():
    git_client = FakeGitClient()
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

    assert git_client.calls == [
        (
            "create_branch",
            "feature/work-item-123",
        ),
        ("stage_all",),
        (
            "commit",
            "feat: implement work item 123",
        ),
        (
            "push",
            "feature/work-item-123",
        ),
    ]

    assert azure_client.calls == [
        (
            "repo-123",
            "feature/work-item-123",
            "main",
            "Implement work item 123",
        )
    ]

    assert len(azure_client.update_calls) == 1

    updated_work_item_id, fields = (
        azure_client.update_calls[0]
    )

    assert updated_work_item_id == 123
    assert "System.History" in fields
    assert "PR 42" in fields["System.History"]

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