from agent.core.azure_boards_publisher import AzureBoardsPublisher
from agent.core.azure_boards_workflow import AzureBoardsWorkflow
from agent.core.work_item_mapper import WorkItemMapper


class FakeAzureDevOpsClient:
    def __init__(self):
        self.pr_calls = []
        self.update_calls = []

    def get_work_item(self, work_item_id):
        return {
            "id": work_item_id,
            "fields": {
                "System.Title": "Add validation support",
                "System.Description": "Update the Python plugin.",
                "System.Tags": "backend; tech:python",
            },
        }

    def get_title(self, work_item):
        return work_item["fields"]["System.Title"]

    def get_description(self, work_item):
        return work_item["fields"]["System.Description"]

    def get_tags(self, work_item):
        raw = work_item["fields"].get(
            "System.Tags",
            "",
        )

        return [
            tag.strip()
            for tag in raw.split(";")
            if tag.strip()
        ]

    def get_technology(self, work_item):
        for tag in self.get_tags(work_item):
            if tag.lower() == "tech:python":
                return "python"

            if tag.lower() == "tech:java":
                return "java"

        return None

    def create_pull_request(
        self,
        repository_id,
        source_branch,
        target_branch,
        title,
        description,
    ):
        self.pr_calls.append(
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


class FakeGitClient:
    def __init__(self):
        self.calls = []
        self.active_branch = "main"
        self.changes = False

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


class FakeAgent:
    def __init__(self, git_client):
        self.received_request = None
        self.git_client = git_client

    def process_request(self, request):
        self.received_request = request

        # Simulate the agent modifying repository files.
        self.git_client.changes = True

        return {
            "plugin": request["technology"],
            "success": True,
        }


def test_azure_boards_end_to_end_workflow():
    azure_client = FakeAzureDevOpsClient()
    git_client = FakeGitClient()

    agent = FakeAgent(
        git_client=git_client,
    )

    mapper = WorkItemMapper(
        azure_client=azure_client,
    )

    publisher = AzureBoardsPublisher(
        git_client=git_client,
        azure_client=azure_client,
        repository_id="repo-123",
    )

    workflow = AzureBoardsWorkflow(
        azure_client=azure_client,
        mapper=mapper,
        agent=agent,
        publisher=publisher,
    )

    result = workflow.execute(
        work_item_id=123,
    )

    assert result["work_item_id"] == 123

    assert result["prepared_branch"] == (
        "feature/work-item-123"
    )

    assert (
        agent.received_request["technology"]
        == "python"
    )

    assert (
        agent.received_request["message"]
        == "Add validation support"
    )

    assert result[
        "agent_result"
    ]["success"] is True

    assert result["published"] is True

    assert result[
        "publish_result"
    ]["branch"] == "feature/work-item-123"

    assert result[
        "publish_result"
    ]["commit"] == "abc123"

    assert result[
        "publish_result"
    ]["pr_id"] == 42

    assert git_client.active_branch == (
        "feature/work-item-123"
    )

    assert azure_client.pr_calls == [
        (
            "repo-123",
            "feature/work-item-123",
            "main",
            "Add validation support",
        )
    ]

    assert len(
        azure_client.update_calls
    ) == 1

    work_item_id, fields = (
        azure_client.update_calls[0]
    )

    assert work_item_id == 123

    assert "System.History" in fields

    assert "PR 42" in fields[
        "System.History"
    ]