from agent.core.code_generator import CodeGenerator
from tests.fakes.fake_llm import FakeLLM


def test_code_generator():
    fake_llm = FakeLLM()
    generator = CodeGenerator(fake_llm)

    request = {
        "message": (
            "Add a validate operation "
            "to the existing Python plugin."
        )
    }

    change = {
        "path": (
            "plugins/python-plugin/"
            "src/python_plugin/main.py"
        ),
        "action": "modify",
        "reason": "Add validate operation routing",
    }

    existing_content = """
class PythonPlugin:
    name = "python"

    def execute(self, request):
        operation = request.get("operation")

        if operation == "analyze":
            return {"success": True}
"""

    repository_context = """
The Python plugin uses execute() to route operations.
Existing operations include analyze, lint, test and execute.
"""

    content = generator.generate_file_content(
        request,
        change,
        existing_content,
        repository_context,
    )

    assert content == (
    'def hello_validation() -> str:\n'
    '    return "hello from live validation"\n'
    )