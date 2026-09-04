"""Coordinate quality checks, repair generation, and retries."""

from agent.core.repair_generator import RepairGenerator
from agent.core.self_healer import SelfHealer
from agent.core.workspace_writer import WorkspaceWriter
from agent.core.quality_gate import QualityGate
from agent.models.proposed_change import ProposedChange
from agent.models.quality_result import QualityResult


class HealingExecutor:
    """Runs quality checks and repairs a proposed change when needed."""

    def __init__(
    self,
    writer: WorkspaceWriter,
    repair_generator: RepairGenerator,
    quality_gate: QualityGate,
    max_attempts: int = 3,
    ) -> None:
        self.writer = writer
        self.repair_generator = repair_generator
        self.quality_gate = quality_gate
        self.self_healer = SelfHealer(max_attempts=max_attempts)

    def execute(
        self,
        request: dict,
        change: ProposedChange,
        repository_context: str,
        technology: str,
    ):
        """Apply, validate, repair, and retry a proposed change."""

        current_change = {"value": change}

        self.writer.apply_proposed_change(current_change["value"])

        def repair(
            quality_result: QualityResult,
            attempt: int,
        ) -> None:
            repaired_change = self.repair_generator.repair_change(
                request=request,
                change=current_change["value"],
                quality_result=quality_result,
                repository_context=repository_context,
            )

            current_change["value"] = repaired_change

            self.writer.apply_proposed_change(
                repaired_change
            )

        result = self.self_healer.run(
            quality_check=lambda: self.quality_gate.run(technology),
            repair=repair,
        )

        if not result.success:
            self.writer.rollback_proposed_change(change)

        return result