"""Convert Azure Boards work items into agent requests."""

from agent.integrations.azure_devops_client import AzureDevOpsClient


class WorkItemMapper:
    """Maps Azure Boards work items into agent request dictionaries."""

    def __init__(
        self,
        azure_client: AzureDevOpsClient,
    ) -> None:
        self.azure_client = azure_client

    def to_agent_request(
        self,
        work_item: dict,
    ) -> dict:
        """Convert a work item into an agent request."""

        title = self.azure_client.get_title(work_item)
        description = self.azure_client.get_description(work_item)
        technology = self.azure_client.get_technology(work_item)
        tags = self.azure_client.get_tags(work_item)

        content_parts = [
            title,
            description,
        ]

        content = "\n\n".join(
            part
            for part in content_parts
            if part
        )

        return {
            "content": content,
            "message": title,
            "technology": technology,
            "tags": tags,
            "work_item_id": work_item.get("id"),
        }