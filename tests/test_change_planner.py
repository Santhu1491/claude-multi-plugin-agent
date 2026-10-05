from agent.core.change_planner import ChangePlanner
from tests.fakes.fake_llm import FakeLLM


def test_change_planner():
    fake_llm = FakeLLM()
    planner = ChangePlanner(fake_llm)

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
"""

    plan = planner.create_change_plan(
        request,
        repository_context,
    )

    assert plan == [
        {
            "path": "agent/utils/live_validation.py",
            "action": "create",
            "reason": "Add requested validation function",
        }
    ]