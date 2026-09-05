from agent.core.work_item_mapper import WorkItemMapper


class FakeAzureClient:
    def get_title(self, work_item):
        return "Add validation support"

    def get_description(self, work_item):
        return "Update the Python plugin."

    def get_technology(self, work_item):
        return "python"

    def get_tags(self, work_item):
        return [
            "backend",
            "tech:python",
        ]


def test_work_item_mapper():
    mapper = WorkItemMapper(
        azure_client=FakeAzureClient(),
    )

    work_item = {
        "id": 123,
    }

    request = mapper.to_agent_request(
        work_item
    )

    assert request["message"] == (
        "Add validation support"
    )

    assert (
        "Update the Python plugin."
        in request["content"]
    )

    assert request["technology"] == "python"

    assert request["work_item_id"] == 123

    assert "tech:python" in request["tags"]