from agent.core.change_planner import ChangePlanner
from agent.integrations.claude import ClaudeClient


def test_change_planner():
    claude = ClaudeClient()
    planner = ChangePlanner(claude)

    request = {
        "message": (
            "Add a validate operation "
            "to the existing Python plugin."
        )
    }

    repository_context = """
--- plugins/python-plugin/src/python_plugin/main.py ---

class PythonPlugin:

    def execute(self, request):
        operation = request.get("operation")

        if operation == "analyze":
            return self.handle_analyze(request)

        if operation == "lint":
            return self.handle_lint(request)
"""

    plan = planner.create_change_plan(
        request,
        repository_context,
    )

    print("\nChange plan:")
    for change in plan:
        print(change)

    assert plan
    assert all(
        change["action"] in {"modify", "create"}
        for change in plan
    )

    assert any(
        "python_plugin" in change["path"]
        for change in plan
    )