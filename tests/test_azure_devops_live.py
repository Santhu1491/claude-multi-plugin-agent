from agent.integrations.azure_devops_client import (
    AzureDevOpsClient,
)


def test_live_get_work_item():
    client = AzureDevOpsClient()

    item = client.get_work_item(
        2  # replace with your actual work item ID
    )

    print("\nWork item:")
    print(item)

    assert item["id"] == 2