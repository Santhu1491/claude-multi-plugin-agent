"""Git and GitHub workflow orchestration."""

from agent.integrations.git_client import GitClient
from agent.integrations.github_client import GitHubClient


class GitWorkflow:
    """Coordinates branch, commit, push, and PR creation."""

    def __init__(
        self,
        git_client: GitClient,
        github_client: GitHubClient,
    ) -> None:
        self.git_client = git_client
        self.github_client = github_client

    def publish_changes(
        self,
        branch_name: str,
        commit_message: str,
        pr_title: str,
        pr_body: str = "",
        base_branch: str = "main",
    ) -> dict:
        """Publish local changes and open a pull request."""

        self.git_client.create_branch(branch_name)
        self.git_client.stage_all()

        commit_hash = self.git_client.commit(
            commit_message
        )

        self.git_client.push(branch_name)

        pr = self.github_client.create_pull_request(
            title=pr_title,
            head=branch_name,
            base=base_branch,
            body=pr_body,
        )

        return {
            "branch": branch_name,
            "commit": commit_hash,
            "pr_number": pr.get("number"),
            "pr_url": pr.get("html_url"),
        }