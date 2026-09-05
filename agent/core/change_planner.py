"""Generate structured repository change plans."""

import json
from typing import Any

from agent.integrations.claude import ClaudeClient


class ChangePlanner:
    """Uses Claude to propose repository file changes."""

    def __init__(self, claude: ClaudeClient) -> None:
        self.claude = claude

    def create_change_plan(
        self,
        request: dict[str, Any],
        repository_context: str,
    ) -> list[dict[str, str]]:
        prompt = f"""
You are planning code changes for a software repository.

Development request:
{request}

Relevant repository context:
{repository_context}

Return ONLY valid JSON.

Use this format:

[
  {{
    "path": "repository/relative/path.py",
    "action": "modify",
    "reason": "short explanation"
  }},
  {{
    "path": "repository/relative/new_file.py",
    "action": "create",
    "reason": "short explanation"
  }}
]

Rules:
- action must be either "modify" or "create"
- use repository-relative paths
- prefer modifying existing files when appropriate
- do not invent unnecessary files
- do not generate source code yet
- return no markdown and no explanation outside the JSON
"""

        response = self.claude.generate(prompt)

        cleaned_response = response.strip()

        if cleaned_response.startswith("```"):
            lines = cleaned_response.splitlines()

            if lines and lines[0].startswith("```"):
                lines = lines[1:]

            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]

            cleaned_response = "\n".join(lines).strip()

        try:
            plan = json.loads(cleaned_response)
        except json.JSONDecodeError as exc:
            raise TypeError(
                "Claude returned an invalid change plan."
            ) from exc

        if not isinstance(plan, list):
            raise TypeError(
                "Change plan must be a list."
            )

        for change in plan:
            if not isinstance(change, dict):
                raise TypeError(
                    "Each change must be an object."
                )

            if change.get("action") not in {
                "modify",
                "create",
            }:
                raise TypeError(
                    "Unsupported change action."
                )

            if not change.get("path"):
                raise TypeError(
                    "Change path is required."
                )

        return plan