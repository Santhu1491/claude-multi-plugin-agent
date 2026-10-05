from agent.core.azure_boards_workflow import AzureBoardsWorkflow


class FakeAzureClient:
    def get_work_item(
        self,
        work_item_id,
    ):
        return {
            "id": work_item_id,
        }


class FakeMapper:
    def to_agent_request(
        self,
        work_item,
    ):
        return {
            "work_item_id": work_item["id"],
            "content": "Update Python plugin",
            "technology": "python",
        }


class FakeAgent:
    def process_request(
        self,
        request,
    ):
        return {
            "plugin": request["technology"],
            "success": True,
        }


class RecordingAgent:
    def __init__(self):
        self.received_request = None

    def process_request(
        self,
        request,
    ):
        self.received_request = request

        return {
            "plugin": request["technology"],
            "success": True,
        }


class FailingAgent:
    def process_request(
        self,
        request,
    ):
        return {
            "plugin": request["technology"],
            "success": False,
        }


class FakePublisher:
    def __init__(self):
        self.prepare_calls = []
        self.publish_calls = []

    def prepare_branch(
        self,
        request,
    ):
        self.prepare_calls.append(
            request
        )

        return (
            f"feature/work-item-"
            f"{request['work_item_id']}"
        )

    def publish(
        self,
        request,
        agent_result,
    ):
        self.publish_calls.append(
            (
                request,
                agent_result,
            )
        )

        return {
            "branch": (
                f"feature/work-item-"
                f"{request['work_item_id']}"
            ),
            "commit": "abc123",
            "pr_id": 42,
        }


def test_azure_boards_workflow():
    workflow = AzureBoardsWorkflow(
        azure_client=FakeAzureClient(),
        mapper=FakeMapper(),
        agent=FakeAgent(),
    )

    result = workflow.execute(
        123
    )

    assert result["work_item_id"] == 123

    assert result[
        "request"
    ]["technology"] == "python"

    assert result[
        "agent_result"
    ]["plugin"] == "python"

    assert result[
        "agent_result"
    ]["success"] is True

    assert result[
        "prepared_branch"
    ] is None

    assert result[
        "published"
    ] is False


def test_azure_boards_workflow_sends_request_to_agent():
    agent = RecordingAgent()

    workflow = AzureBoardsWorkflow(
        azure_client=FakeAzureClient(),
        mapper=FakeMapper(),
        agent=agent,
    )

    result = workflow.execute(
        123
    )

    assert agent.received_request is not None

    assert agent.received_request[
        "work_item_id"
    ] == 123

    assert agent.received_request[
        "technology"
    ] == "python"

    assert result[
        "agent_result"
    ]["plugin"] == "python"


def test_azure_boards_workflow_publishes_result():
    publisher = FakePublisher()

    workflow = AzureBoardsWorkflow(
        azure_client=FakeAzureClient(),
        mapper=FakeMapper(),
        agent=RecordingAgent(),
        publisher=publisher,
    )

    result = workflow.execute(
        123
    )

    assert len(
        publisher.prepare_calls
    ) == 1

    assert len(
        publisher.publish_calls
    ) == 1

    assert result[
        "prepared_branch"
    ] == "feature/work-item-123"

    assert result[
        "published"
    ] is True

    assert result[
        "publish_result"
    ] == {
        "branch": "feature/work-item-123",
        "commit": "abc123",
        "pr_id": 42,
    }


def test_azure_boards_workflow_does_not_publish_failed_agent():
    publisher = FakePublisher()

    workflow = AzureBoardsWorkflow(
        azure_client=FakeAzureClient(),
        mapper=FakeMapper(),
        agent=FailingAgent(),
        publisher=publisher,
    )

    result = workflow.execute(
        123
    )

    assert result[
        "success"
    ] is False

    assert result[
        "published"
    ] is False

    assert result[
        "publish_result"
    ] is None

    assert result[
        "prepared_branch"
    ] == "feature/work-item-123"

    assert len(
        publisher.prepare_calls
    ) == 1

    assert publisher.publish_calls == []