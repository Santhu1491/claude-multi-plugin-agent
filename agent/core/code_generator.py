"""Generate source code for planned repository changes."""

from typing import Any

# from agent.integrations.claude import ClaudeClient
from agent.integrations.llm import LLMClient


class CodeGenerator:
    """Uses Claude to generate complete file contents."""

    def __init__(self, claude: LLMClient) -> None:
        self.claude = claude

    def generate_file_content(
        self,
        request: dict[str, Any],
        change: dict[str, str],
        existing_content: str | None,
        repository_context: str,
    ) -> str:
        prompt = f"""
You are modifying a software repository.

Development request:
{request}

Planned change:
Path: {change["path"]}
Action: {change["action"]}
Reason: {change["reason"]}

Relevant repository context:
{repository_context}

Existing file content:
{existing_content if existing_content is not None else "[NEW FILE]"}

Generate the COMPLETE final content for this file.

Rules:
- Return only the file content.
- Do not use markdown code fences.
- Do not explain the change.
- Preserve existing behavior unless required by the request.
- Follow the style and architecture of the existing repository.
- Do not modify unrelated functionality.
- Make the smallest implementation necessary to satisfy the request.
- Do not add new third-party dependencies unless explicitly required by the request or change plan.
- Do not introduce new frameworks, HTTP servers, CLI modes, infrastructure, or architectural patterns unless explicitly requested.
- Do not add or update documentation unless explicitly requested.
- Preserve existing entrypoints unless changing them is necessary.
"""

        content = self.claude.generate(prompt)

        if not content.strip():
            raise ValueError(
                f"Claude returned empty content for {change['path']}"
            )

        return content