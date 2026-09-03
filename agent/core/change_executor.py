"""Coordinate planning, generation, diffing, and application of changes."""

from agent.core.change_builder import ChangeBuilder
from agent.core.change_planner import ChangePlanner
from agent.core.workspace import Workspace
from agent.core.workspace_writer import WorkspaceWriter


class ChangeExecutor:
    """Executes repository changes in a controlled workflow."""

    def __init__(
        self,
        workspace: Workspace,
        writer: WorkspaceWriter,
        planner: ChangePlanner,
        builder: ChangeBuilder,
    ) -> None:
        self.workspace = workspace
        self.writer = writer
        self.planner = planner
        self.builder = builder

    def execute(
        self,
        request: dict,
        repository_context: str,
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
                results.append(
                    self.writer.apply_proposed_change(change)
                )

        return {
            "plan": validated_plan,
            "changes": proposed_changes,
            "diffs": diffs,
            "applied": apply_changes,
            "results": results,
        }