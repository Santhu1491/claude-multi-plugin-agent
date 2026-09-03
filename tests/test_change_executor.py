from pathlib import Path

from agent.core.change_executor import ChangeExecutor
from agent.core.workspace import Workspace
from agent.core.workspace_writer import WorkspaceWriter
from agent.models.proposed_change import ProposedChange


class FakePlanner:
    def create_change_plan(
        self,
        request,
        repository_context,
    ):
        return [
            {
                "path": "app.py",
                "action": "modify",
                "reason": "Update application",
            }
        ]


class FakeBuilder:
    def build_changes(
        self,
        request,
        change_plan,
        repository_context,
    ):
        return [
            ProposedChange(
                path="app.py",
                action="modify",
                reason="Update application",
                original_content="old content",
                generated_content="new content",
            )
        ]


def test_change_executor_preview(tmp_path: Path):
    (tmp_path / "app.py").write_text(
        "old content",
        encoding="utf-8",
    )

    workspace = Workspace(tmp_path)
    writer = WorkspaceWriter(tmp_path)

    executor = ChangeExecutor(
        workspace=workspace,
        writer=writer,
        planner=FakePlanner(),
        builder=FakeBuilder(),
    )

    result = executor.execute(
        request={"message": "Update app"},
        repository_context="test context",
        apply_changes=False,
    )

    assert result["applied"] is False
    assert result["diffs"]

    assert (
        tmp_path / "app.py"
    ).read_text(encoding="utf-8") == "old content"


def test_change_executor_applies_changes(
    tmp_path: Path,
):
    (tmp_path / "app.py").write_text(
        "old content",
        encoding="utf-8",
    )

    workspace = Workspace(tmp_path)
    writer = WorkspaceWriter(tmp_path)

    executor = ChangeExecutor(
        workspace=workspace,
        writer=writer,
        planner=FakePlanner(),
        builder=FakeBuilder(),
    )

    result = executor.execute(
        request={"message": "Update app"},
        repository_context="test context",
        apply_changes=True,
    )

    assert result["applied"] is True

    assert (
        tmp_path / "app.py"
    ).read_text(encoding="utf-8") == "new content"