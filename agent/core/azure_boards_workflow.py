"""Azure Boards work item execution workflow."""

from agent.core.work_item_mapper import WorkItemMapper
from agent.integrations.azure_devops_client import AzureDevOpsClient


class AzureBoardsWorkflow:
    """Fetches an Azure Boards work item and sends it to the agent."""

    def __init__(
        self,
        azure_client: AzureDevOpsClient,
        mapper: WorkItemMapper,
        agent,
        publisher=None,
    ) -> None:
        self.azure_client = azure_client
        self.mapper = mapper
        self.agent = agent
        self.publisher = publisher

    def execute(self, work_item_id: int) -> dict:
        """Process a single Azure Boards work item."""

        work_item = self.azure_client.get_work_item(
            work_item_id
        )

        request = self.mapper.to_agent_request(
            work_item
        )

        prepared_branch = None

        if self.publisher is not None:
            prepared_branch = self.publisher.prepare_branch(
                request
            )

        agent_result = self.agent.process_request(
            request
        )

        publish_result = None
        published = False

        if (
            self.publisher is not None
            and agent_result.get("success", False)
        ):
            publish_result = self.publisher.publish(
                request=request,
                agent_result=agent_result,
            )
            published = True

        return {
            "work_item_id": work_item_id,
            "request": request,
            "prepared_branch": prepared_branch,
            "agent_result": agent_result,
            "published": published,
            "publish_result": publish_result,
            "success": agent_result.get(
                "success",
                False,
            ),
        }