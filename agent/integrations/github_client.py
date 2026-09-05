"""GitHub pull request integration."""

import os

import requests


class GitHubClient:
    """Minimal GitHub API client."""

    def __init__(
        self,
        owner: str,
        repo: str,
        token: str | None = None,
    ) -> None:
        self.owner = owner
        self.repo = repo
        self.token = token or os.getenv("GITHUB_TOKEN")

        if not self.token:
            raise ValueError("GITHUB_TOKEN is not configured.")

        self.base_url = (
            f"https://api.github.com/repos/"
            f"{self.owner}/{self.repo}"
        )

    def create_pull_request(
        self,
        title: str,
        head: str,
        base: str = "main",
        body: str = "",
    ) -> dict:
        """Create a GitHub pull request."""

        response = requests.post(
            f"{self.base_url}/pulls",
            headers={
                "Authorization": f"Bearer {self.token}",
                "Accept": "application/vnd.github+json",
            },
            json={
                "title": title,
                "head": head,
                "base": base,
                "body": body,
            },
            timeout=30,
        )

        if response.status_code not in {200, 201}:
            raise RuntimeError(
                f"GitHub PR creation failed: "
                f"{response.status_code} "
                f"{response.text}"
            )

        return response.json()