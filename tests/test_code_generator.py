from agent.core.code_generator import CodeGenerator
from agent.integrations.claude import ClaudeClient


def test_code_generator():
    claude = ClaudeClient()
    generator = CodeGenerator(claude)

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

    print("\nGenerated content:")
    print(content)

    assert content
    assert "PythonPlugin" in content
    assert "validate" in content