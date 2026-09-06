import os

import pytest

from agent.config.settings import Settings
from agent.core.agent import Agent
from agent.core.azure_boards_publisher import AzureBoardsPublisher
from agent.core.azure_boards_workflow import AzureBoardsWorkflow
from agent.core.work_item_mapper import WorkItemMapper
from agent.integrations.azure_devops_client import AzureDevOpsClient
from agent.integrations.git_client import GitClient

pytestmark = pytest.mark.live


def test_live_azure_boards_end_to_end():
    work_item_id = os.getenv("AZURE_DEVOPS_TEST_WORK_ITEM_ID")

    if not work_item_id:
        pytest.skip(
            "AZURE_DEVOPS_TEST_WORK_ITEM_ID is not configured"
        )

    repository_id = os.getenv("AZURE_DEVOPS_REPOSITORY")

    if not repository_id:
        pytest.skip(
            "AZURE_DEVOPS_REPOSITORY is not configured"
        )

    settings = Settings()

    azure_client = AzureDevOpsClient()
    agent = Agent(settings)
    mapper = WorkItemMapper(azure_client)

    git_client = GitClient(
        ".",
        remote_name="azure",
    )

    publisher = AzureBoardsPublisher(
        git_client=git_client,
        azure_client=azure_client,
        repository_id=repository_id,
    )

    workflow = AzureBoardsWorkflow(
        azure_client=azure_client,
        mapper=mapper,
        agent=agent,
        publisher=publisher,
    )

    result = workflow.execute(
        int(work_item_id)
    )

    assert result["success"] is True
    assert result["published"] is True
    assert result["publish_result"] is not None
    assert result["publish_result"]["pr_id"] is not None