from agent.core.azure_boards_workflow import (
    AzureBoardsWorkflow,
)


class FakeAzureClient:
    def get_work_item(self, work_item_id):
        return {
            "id": work_item_id,
        }


class FakeMapper:
    def to_agent_request(self, work_item):
        return {
            "work_item_id": work_item["id"],
            "content": "Update Python plugin",
            "technology": "python",
        }


class FakeAgent:
    def process_request(self, request):
        return {
            "plugin": request["technology"],
            "success": True,
        }


def test_azure_boards_workflow():
    workflow = AzureBoardsWorkflow(
        azure_client=FakeAzureClient(),
        mapper=FakeMapper(),
        agent=FakeAgent(),
    )

    result = workflow.execute(123)

    assert result["work_item_id"] == 123
    assert result["request"]["technology"] == "python"
    assert result["result"]["plugin"] == "python"
    assert result["result"]["success"] is True

from agent.core.azure_boards_workflow import AzureBoardsWorkflow


class FakeAzureClient:
    def get_work_item(self, work_item_id):
        return {
            "id": work_item_id,
        }


class FakeMapper:
    def to_agent_request(self, work_item):
        return {
            "work_item_id": work_item["id"],
            "content": "Update Python plugin",
            "technology": "python",
        }


class RecordingAgent:
    def __init__(self):
        self.received_request = None

    def process_request(self, request):
        self.received_request = request

        return {
            "plugin": request["technology"],
            "success": True,
        }


def test_azure_boards_workflow_sends_request_to_agent():
    agent = RecordingAgent()

    workflow = AzureBoardsWorkflow(
        azure_client=FakeAzureClient(),
        mapper=FakeMapper(),
        agent=agent,
    )

    result = workflow.execute(123)

    assert agent.received_request is not None
    assert agent.received_request["work_item_id"] == 123
    assert agent.received_request["technology"] == "python"

    assert result["result"]["plugin"] == "python"

class FakePublisher:
    def __init__(self):
        self.calls = []

    def publish(
        self,
        request,
        agent_result,
    ):
        self.calls.append(
            (request, agent_result)
        )

        return {
            "branch": "feature/123",
            "commit": "abc123",
        }


def test_azure_boards_workflow_publishes_result():
    publisher = FakePublisher()

    workflow = AzureBoardsWorkflow(
        azure_client=FakeAzureClient(),
        mapper=FakeMapper(),
        agent=RecordingAgent(),
        publisher=publisher,
    )

    result = workflow.execute(123)

    assert len(publisher.calls) == 1

    assert result["publish_result"] == {
        "branch": "feature/123",
        "commit": "abc123",
    }