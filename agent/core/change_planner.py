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

        try:
            plan = json.loads(response)
        except json.JSONDecodeError as exc:
            raise ValueError(
                "Claude returned an invalid change plan."
            ) from exc

        if not isinstance(plan, list):
            raise ValueError(
                "Change plan must be a list."
            )

        for change in plan:
            if not isinstance(change, dict):
                raise ValueError(
                    "Each change must be an object."
                )

            if change.get("action") not in {
                "modify",
                "create",
            }:
                raise ValueError(
                    "Unsupported change action."
                )

            if not change.get("path"):
                raise ValueError(
                    "Change path is required."
                )

        return plan