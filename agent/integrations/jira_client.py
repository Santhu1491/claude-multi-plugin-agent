"""Jira Cloud integration."""

import os
import requests


class JiraClient:
    """Minimal Jira Cloud API client."""

    def __init__(
        self,
        base_url: str,
        email: str | None = None,
        api_token: str | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.email = email or os.getenv("JIRA_EMAIL")
        self.api_token = api_token or os.getenv("JIRA_API_TOKEN")

        if not self.email:
            raise ValueError("JIRA_EMAIL is not configured.")

        if not self.api_token:
            raise ValueError("JIRA_API_TOKEN is not configured.")

    def get_issue(self, issue_key: str) -> dict:
        """Fetch a Jira issue."""

        response = requests.get(
            f"{self.base_url}/rest/api/3/issue/{issue_key}",
            auth=(
                self.email,
                self.api_token,
            ),
            headers={
                "Accept": "application/json",
            },
            timeout=30,
        )

        if response.status_code != 200:
            raise RuntimeError(
                f"Jira issue fetch failed: "
                f"{response.status_code} "
                f"{response.text}"
            )

        return response.json()