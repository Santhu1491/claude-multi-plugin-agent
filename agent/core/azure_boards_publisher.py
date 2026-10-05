"""Publish successful Azure Boards changes through Git."""

from agent.integrations.azure_devops_client import AzureDevOpsClient
from agent.integrations.git_client import GitClient


class AzureBoardsPublisher:
    """Creates, commits, pushes, and publishes Azure Boards changes."""

    def __init__(
        self,
        git_client: GitClient,
        azure_client: AzureDevOpsClient,
        repository_id: str,
        base_branch: str = "main",
    ) -> None:
        self.git_client = git_client
        self.azure_client = azure_client
        self.repository_id = repository_id
        self.base_branch = base_branch

    def prepare_branch(
        self,
        request: dict,
    ) -> str:
        """Create the work-item branch before repository changes begin."""

        if self.git_client.has_changes():
            raise RuntimeError(
                "Working tree must be clean before starting agent execution."
            )

        current_branch = self.git_client.current_branch()

        if current_branch != self.base_branch:
            raise RuntimeError(
                f"Agent execution must start from "
                f"'{self.base_branch}', not '{current_branch}'."
            )

        work_item_id = request.get("work_item_id")

        if work_item_id is None:
            raise ValueError(
                "work_item_id is required to create a feature branch."
            )

        branch_name = (
            f"feature/work-item-{work_item_id}"
        )

        self.git_client.create_branch(
            branch_name
        )

        self.git_client.ensure_safe_branch()

        return branch_name

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

        if work_item_id is None:
            raise ValueError(
                "work_item_id is required to publish changes."
            )

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

        current_branch = self.git_client.current_branch()

        if current_branch != branch_name:
            raise RuntimeError(
                f"Expected active branch '{branch_name}', "
                f"but found '{current_branch}'."
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
            target_branch=self.base_branch,
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