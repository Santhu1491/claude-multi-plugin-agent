"""Coordinate planning, generation, diffing, and application of changes."""

from agent.core.change_builder import ChangeBuilder
from agent.core.change_planner import ChangePlanner
from agent.core.workspace import Workspace
from agent.core.workspace_writer import WorkspaceWriter
from agent.core.healing_executor import HealingExecutor
from agent.core.quality_gate import QualityGate
from agent.core.repair_generator import RepairGenerator
from agent.integrations.claude import ClaudeClient


class ChangeExecutor:
    """Executes repository changes in a controlled workflow."""

    def __init__(
        self,
        workspace: Workspace,
        writer: WorkspaceWriter,
        planner: ChangePlanner,
        builder: ChangeBuilder,
        claude: ClaudeClient,
    ) -> None:
        self.workspace = workspace
        self.writer = writer
        self.planner = planner
        self.builder = builder

        quality_gate = QualityGate(workspace.root)
        repair_generator = RepairGenerator(claude)

        self.healing_executor = HealingExecutor(
            writer=writer,
            repair_generator=repair_generator,
            quality_gate=quality_gate,
            max_attempts=3,
        )

    def execute(
        self,
        request: dict,
        repository_context: str,
        technology: str,
        apply_changes: bool = False,
    ) -> dict:
        plan = self.planner.create_change_plan(
            request,
            repository_context,
        )

        validated_plan = self.writer.validate_change_plan(plan)

        proposed_changes = self.builder.build_changes(
            request=request,
            change_plan=validated_plan,
            repository_context=repository_context,
        )

        diffs = [
            change.build_diff()
            for change in proposed_changes
        ]

        results = []

        if apply_changes:
            for change in proposed_changes:
                healing_result = self.healing_executor.execute(
                    request=request,
                    change=change,
                    repository_context=repository_context,
                    technology=technology,
                )
        
                results.append(healing_result)

        return {
            "plan": validated_plan,
            "changes": proposed_changes,
            "diffs": diffs,
            "applied": apply_changes,
            "results": results,
        }