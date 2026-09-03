from pathlib import Path

from agent.core.change_builder import ChangeBuilder
from agent.core.workspace import Workspace


class FakeGenerator:
    def generate_file_content(
        self,
        request,
        change,
        existing_content,
        repository_context,
    ):
        return "generated content"


def test_change_builder(tmp_path: Path):
    file_path = tmp_path / "app.py"

    file_path.write_text(
        "original content",
        encoding="utf-8",
    )

    workspace = Workspace(tmp_path)
    generator = FakeGenerator()

    builder = ChangeBuilder(
        workspace,
        generator,
    )

    plan = [
        {
            "path": "app.py",
            "action": "modify",
            "reason": "Update application",
        },
        {
            "path": "new.py",
            "action": "create",
            "reason": "Create new module",
        },
    ]

    changes = builder.build_changes(
        request={"message": "Update project"},
        change_plan=plan,
        repository_context="test context",
    )

    assert len(changes) == 2

    assert changes[0].original_content == "original content"
    assert changes[0].generated_content == "generated content"

    assert changes[1].original_content is None
    assert changes[1].generated_content == "generated content"