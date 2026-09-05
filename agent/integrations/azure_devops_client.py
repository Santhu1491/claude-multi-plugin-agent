"""Azure DevOps integration client."""

import os

import requests
from dotenv import load_dotenv

load_dotenv()


class AzureDevOpsClient:
    """Minimal Azure DevOps client configuration."""

    def __init__(
        self,
        organization: str | None = None,
        project: str | None = None,
        pat: str | None = None,
    ) -> None:
        self.organization = (
            organization
            or os.getenv("AZURE_DEVOPS_ORG")
        )

        self.project = (
            project
            or os.getenv("AZURE_DEVOPS_PROJECT")
        )

        self.pat = (
            pat
            or os.getenv("AZURE_DEVOPS_PAT")
        )

        if not self.organization:
            raise ValueError(
                "AZURE_DEVOPS_ORG is not configured."
            )

        if not self.project:
            raise ValueError(
                "AZURE_DEVOPS_PROJECT is not configured."
            )

        if not self.pat:
            raise ValueError(
                "AZURE_DEVOPS_PAT is not configured."
            )

        self.base_url = (
            f"https://dev.azure.com/"
            f"{self.organization}/"
            f"{self.project}"
        )

    def get_work_item(self, work_item_id: int) -> dict:
        """Fetch an Azure Boards work item."""

        url = (
            f"{self.base_url}/_apis/wit/workitems/"
            f"{work_item_id}?api-version=7.1"
        )

        response = requests.get(
            url,
            auth=("", self.pat),
            headers={
                "Accept": "application/json",
            },
            timeout=30,
        )

        if response.status_code != 200:
            raise RuntimeError(
                f"Azure DevOps work item fetch failed: "
                f"{response.status_code} {response.text}"
            )

        return response.json()

    def get_title(self, work_item: dict) -> str:
        """Return the work item title."""

        return work_item.get(
            "fields",
            {},
        ).get(
            "System.Title",
            "",
        )


    def get_description(self, work_item: dict) -> str:
        """Return the work item description."""

        return work_item.get(
            "fields",
            {},
        ).get(
            "System.Description",
            "",
        )


    def get_tags(self, work_item: dict) -> list[str]:
        """Return Azure Boards tags as a list."""

        raw_tags = work_item.get(
            "fields",
            {},
        ).get(
            "System.Tags",
            "",
        )

        if not raw_tags:
            return []

        return [
            tag.strip()
            for tag in raw_tags.split(";")
            if tag.strip()
        ]


    def get_technology(self, work_item: dict) -> str | None:
        """Extract python/java technology from work item tags."""

        for tag in self.get_tags(work_item):
            normalized = tag.lower()

            if normalized in {"python", "tech:python"}:
                return "python"

            if normalized in {"java", "tech:java"}:
                return "java"

        return None

    def test_extract_work_item_fields():
        client = AzureDevOpsClient(
            organization="test-org",
            project="test-project",
            pat="fake-pat",
        )

        work_item = {
            "fields": {
                "System.Title": "Add validation support",
                "System.Description": "Update the Python plugin.",
                "System.Tags": "backend; tech:python; automation",
            }
        }

        assert (
            client.get_title(work_item)
            == "Add validation support"
        )

        assert (
            client.get_description(work_item)
            == "Update the Python plugin."
        )

        assert client.get_tags(work_item) == [
            "backend",
            "tech:python",
            "automation",
        ]

        assert (
            client.get_technology(work_item)
            == "python"
        )

    def create_pull_request(
        self,
        repository_id: str,
        source_branch: str,
        target_branch: str = "main",
        title: str = "",
        description: str = "",
    ) -> dict:
        """Create a pull request in Azure Repos."""
    
        url = (
            f"{self.base_url}/_apis/git/repositories/"
            f"{repository_id}/pullrequests"
            f"?api-version=7.1"
        )
    
        payload = {
            "sourceRefName": f"refs/heads/{source_branch}",
            "targetRefName": f"refs/heads/{target_branch}",
            "title": title,
            "description": description,
        }
    
        response = requests.post(
            url,
            auth=("", self.pat),
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=30,
        )
    
        if response.status_code not in {200, 201}:
            raise RuntimeError(
                f"Azure DevOps PR creation failed: "
                f"{response.status_code} {response.text}"
            )
    
        return response.json()

    def update_work_item(
        self,
        work_item_id: int,
        fields: dict[str, str],
    ) -> dict:
        """Update fields on an Azure Boards work item."""
    
        url = (
            f"{self.base_url}/_apis/wit/workitems/"
            f"{work_item_id}?api-version=7.1"
        )
    
        patch_document = [
            {
                "op": "add",
                "path": f"/fields/{field_name}",
                "value": value,
            }
            for field_name, value in fields.items()
        ]
    
        response = requests.patch(
            url,
            auth=("", self.pat),
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json-patch+json",
            },
            json=patch_document,
            timeout=30,
        )
    
        if response.status_code != 200:
            raise RuntimeError(
                f"Azure DevOps work item update failed: "
                f"{response.status_code} {response.text}"
            )
    
        return response.json()