from agent.core.file_selector import FileSelector
from tests.fakes.fake_llm import FakeLLM


def test_file_selector():
    claude = FakeLLM()
    selector = FileSelector(claude)

    file_tree = """
Repository files:
- agent/core/agent.py
- agent/core/workspace.py
- agent/core/router.py
- plugins/python-plugin/src/python_plugin/main.py
- plugins/python-plugin/src/python_plugin/tools/linter.py
- plugins/java-plugin/src/main/java/com/claude/plugin/java/Main.java
- README.md
"""

    request = {
        "message":
            "Add a validate operation to the existing Python plugin."
    }

    files = selector.select_files(
        request,
        file_tree,
    )

    assert files
    assert files == ["agent/utils/__init__.py"]