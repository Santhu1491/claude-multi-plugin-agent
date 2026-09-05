"""Task execution engine."""

from typing import Any

from agent.core.context import Context
from agent.models.task import Task


class Executor:
    """Executes planned tasks using appropriate plugins."""

    def __init__(self) -> None:
        self.plugins: dict[str, Any] = {}

    def register_plugin(self, name: str, plugin: Any) -> None:
        """Register a plugin for execution."""
        self.plugins[name] = plugin

    def execute(self, tasks: list[Task], context: Context) -> dict[str, Any]:
        """Execute a list of tasks."""
        results = []
        
        for task in tasks:
            plugin = self.plugins.get(task.plugin)
            if not plugin:
                results.append({
                    "success": False,
                    "error": f"Plugin '{task.plugin}' not found"
                })
                continue
            
            # Execute the task with the plugin
            result = self._execute_task(plugin, task, context)
            results.append(result)
        
        return {
            "success": all(r.get("success", False) for r in results),
            "results": results
        }

    def _execute_task(self, plugin: Any, task: Task, context: Context) -> dict[str, Any]:
        """Execute a single task."""
        try:
            # Call plugin's execute method
            if hasattr(plugin, "execute"):
                return plugin.execute({
                    "operation": task.operation,
                    "parameters": task.parameters
                })
            return {"success": False, "error": "Plugin has no execute method"}
        except Exception as e:  # noqa: BLE001
            return {"success": False, "error": str(e)}
