"""Publish successful Azure Boards changes through Git."""

from agent.integrations.azure_devops_client import AzureDevOpsClient
from agent.integrations.git_client import GitClient


class AzureBoardsPublisher:
    """Creates a branch, commits changes, and pushes them."""

    def __init__(
        self,
        git_client: GitClient,
        azure_client: AzureDevOpsClient,
        repository_id: str,
    ) -> None:
        self.git_client = git_client
        self.azure_client = azure_client
        self.repository_id = repository_id

    def publish(
        self,
        request: dict,
        agent_result: dict,
    ) -> dict:
        """Publish successful agent changes."""

        if not agent_result.get("success", False):
            raise RuntimeError(
                "Agent execution failed. Changes will not be published."
            )

        work_item_id = request.get("work_item_id")

        branch_name = (
            f"feature/work-item-{work_item_id}"
        )

        commit_message = (
            f"feat: implement work item {work_item_id}"
        )

        pr_title = (
            request.get("message")
            or f"Implement work item {work_item_id}"
        )

        if not self.git_client.has_changes():
            raise RuntimeError(
                "No repository changes available to publish."
            )

        self.git_client.create_branch(
            branch_name
        )

        self.git_client.ensure_safe_branch()

        commit_hash = self.git_client.commit(
            commit_message
        )

        self.git_client.push(
            branch_name
        )

        pr = self.azure_client.create_pull_request(
            repository_id=self.repository_id,
            source_branch=branch_name,
            target_branch="main",
            title=pr_title,
            description=(
                f"Automated implementation for "
                f"Azure Boards work item {work_item_id}"
            ),
        )

        pr_id = pr.get("pullRequestId")

        self.azure_client.update_work_item(
            work_item_id=work_item_id,
            fields={
                "System.History": (
                    f"Automated PR {pr_id} created "
                    f"from branch {branch_name}."
                )
            },
        )

        return {
            "branch": branch_name,
            "commit": commit_hash,
            "pr_id": pr_id,
        }