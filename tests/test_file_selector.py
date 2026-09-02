from agent.core.file_selector import FileSelector
from agent.integrations.claude import ClaudeClient


def test_file_selector():
    claude = ClaudeClient()
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

    print("\nSelected files:")
    for file in files:
        print(file)

    assert files
    assert any(
        "python_plugin" in file
        for file in files
    )