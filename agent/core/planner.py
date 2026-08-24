"""Task planning and decomposition."""

from typing import Any
from agent.models.task import Task


class Planner:
    """Decomposes requests into executable tasks."""

    def create_plan(self, request: dict[str, Any], plugin_name: str) -> list[Task]:
        """Create an execution plan from a request."""
        # Simple single-task plan for now
        task = Task(
            plugin=plugin_name,
            operation=request.get("operation", "execute"),
            parameters=request.get("parameters", {}),
            priority=1
        )
        return [task]

    def optimize_plan(self, tasks: list[Task]) -> list[Task]:
        """Optimize task execution order."""
        # Sort by priority for now
        return sorted(tasks, key=lambda t: t.priority, reverse=True)
