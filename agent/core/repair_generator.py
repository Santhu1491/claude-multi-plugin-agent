"""Generate repaired source code after quality gate failures."""

from typing import Any

from agent.integrations.claude import ClaudeClient
from agent.models.proposed_change import ProposedChange
from agent.models.quality_result import QualityResult


class RepairGenerator:
    """Uses Claude to repair generated code using quality gate feedback."""

    def __init__(self, claude: ClaudeClient) -> None:
        self.claude = claude

    def repair_change(
        self,
        request: dict[str, Any],
        change: ProposedChange,
        quality_result: QualityResult,
        repository_context: str,
    ) -> ProposedChange:
        """Generate a repaired version of a proposed change."""

        prompt = f"""
You are repairing a software repository change.

Development request:
{request}

File:
{change.path}

Reason for change:
{change.reason}

Current generated content:
{change.generated_content}

Quality checks run:
{quality_result.checks_run}

Quality output:
{quality_result.output}

Quality errors:
{quality_result.errors}

Relevant repository context:
{repository_context}

Generate the COMPLETE corrected content for the file.

Rules:
- Fix the reported quality failure.
- Preserve the original requested functionality.
- Do not modify unrelated behavior.
- Return only the complete file content.
- Do not use markdown code fences.
- Do not include explanations.
"""

        repaired_content = self.claude.generate(prompt)

        if not repaired_content.strip():
            raise ValueError(
                f"Claude returned empty repair content for {change.path}"
            )

        return ProposedChange(
            path=change.path,
            action=change.action,
            reason=change.reason,
            original_content=change.original_content,
            generated_content=repaired_content,
        )