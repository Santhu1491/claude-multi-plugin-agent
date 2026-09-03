from pathlib import Path

import pytest

from agent.core.workspace_writer import WorkspaceWriter
from agent.models.proposed_change import ProposedChange


def test_writer_creates_file(tmp_path: Path):
    writer = WorkspaceWriter(tmp_path)

    result = writer.write_file(
        "src/app.py",
        "print('hello')",
    )

    assert result["success"] is True
    assert result["created"] is True

    created_file = tmp_path / "src" / "app.py"

    assert created_file.exists()
    assert created_file.read_text(
        encoding="utf-8"
    ) == "print('hello')"


def test_writer_updates_existing_file(tmp_path: Path):
    file_path = tmp_path / "app.py"

    file_path.write_text(
        "old content",
        encoding="utf-8",
    )

    writer = WorkspaceWriter(tmp_path)

    result = writer.write_file(
        "app.py",
        "new content",
    )

    assert result["created"] is False
    assert result["original_content"] == "old content"
    assert result["new_content"] == "new content"

    assert file_path.read_text(
        encoding="utf-8"
    ) == "new content"


def test_writer_creates_parent_directories(
    tmp_path: Path,
):
    writer = WorkspaceWriter(tmp_path)

    writer.write_file(
        "src/services/customer.py",
        "class CustomerService:\n    pass",
    )

    assert (
        tmp_path
        / "src"
        / "services"
        / "customer.py"
    ).exists()


def test_writer_blocks_parent_directory_access(
    tmp_path: Path,
):
    writer = WorkspaceWriter(tmp_path)

    with pytest.raises(ValueError):
        writer.write_file(
            "../outside.py",
            "malicious",
        )

def test_writer_validates_modify_existing_file(
    tmp_path: Path,
):
    file_path = tmp_path / "app.py"
    file_path.write_text(
        "print('hello')",
        encoding="utf-8",
    )

    writer = WorkspaceWriter(tmp_path)

    plan = [
        {
            "path": "app.py",
            "action": "modify",
            "reason": "Update application",
        }
    ]

    validated = writer.validate_change_plan(plan)

    assert validated == plan


def test_writer_rejects_modify_missing_file(
    tmp_path: Path,
):
    writer = WorkspaceWriter(tmp_path)

    plan = [
        {
            "path": "missing.py",
            "action": "modify",
            "reason": "Update missing file",
        }
    ]

    with pytest.raises(ValueError):
        writer.validate_change_plan(plan)


def test_writer_rejects_create_existing_file(
    tmp_path: Path,
):
    (tmp_path / "app.py").write_text(
        "existing",
        encoding="utf-8",
    )

    writer = WorkspaceWriter(tmp_path)

    plan = [
        {
            "path": "app.py",
            "action": "create",
            "reason": "Create app",
        }
    ]

    with pytest.raises(ValueError):
        writer.validate_change_plan(plan)

def test_writer_applies_proposed_change(
    tmp_path: Path,
):
    file_path = tmp_path / "app.py"

    file_path.write_text(
        "old content",
        encoding="utf-8",
    )

    writer = WorkspaceWriter(tmp_path)

    change = ProposedChange(
        path="app.py",
        action="modify",
        reason="Update app",
        original_content="old content",
        generated_content="new content",
    )

    result = writer.apply_proposed_change(change)

    assert result["success"] is True
    assert file_path.read_text(
        encoding="utf-8"
    ) == "new content"


def test_writer_rolls_back_modified_file(
    tmp_path: Path,
):
    file_path = tmp_path / "app.py"

    file_path.write_text(
        "old content",
        encoding="utf-8",
    )

    writer = WorkspaceWriter(tmp_path)

    change = ProposedChange(
        path="app.py",
        action="modify",
        reason="Update app",
        original_content="old content",
        generated_content="new content",
    )

    writer.apply_proposed_change(change)
    writer.rollback_proposed_change(change)

    assert file_path.read_text(
        encoding="utf-8"
    ) == "old content"


def test_writer_rolls_back_created_file(
    tmp_path: Path,
):
    writer = WorkspaceWriter(tmp_path)

    change = ProposedChange(
        path="new.py",
        action="create",
        reason="Create file",
        original_content=None,
        generated_content="print('hello')",
    )

    writer.apply_proposed_change(change)

    created_file = tmp_path / "new.py"

    assert created_file.exists()

    writer.rollback_proposed_change(change)

    assert not created_file.exists()