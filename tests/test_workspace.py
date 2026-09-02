from pathlib import Path

from agent.core.workspace import Workspace


def test_workspace_lists_files(tmp_path: Path):
    (tmp_path / "app.py").write_text(
        "print('hello')",
        encoding="utf-8",
    )

    (tmp_path / "README.md").write_text(
        "# Test Project",
        encoding="utf-8",
    )

    workspace = Workspace(tmp_path)

    files = workspace.list_files()

    assert "app.py" in files
    assert "README.md" in files


def test_workspace_ignores_git_directory(tmp_path: Path):
    git_dir = tmp_path / ".git"
    git_dir.mkdir()

    (git_dir / "config").write_text(
        "git config",
        encoding="utf-8",
    )

    workspace = Workspace(tmp_path)

    files = workspace.list_files()

    assert ".git/config" not in files


def test_workspace_reads_file(tmp_path: Path):
    (tmp_path / "app.py").write_text(
        "print('hello')",
        encoding="utf-8",
    )

    workspace = Workspace(tmp_path)

    content = workspace.read_file("app.py")

    assert content == "print('hello')"


def test_workspace_blocks_parent_directory_access(tmp_path: Path):
    workspace = Workspace(tmp_path)

    try:
        workspace.read_file("../secret.txt")
        assert False, "Expected workspace boundary protection"
    except ValueError:
        pass

def test_workspace_builds_summary(tmp_path: Path):
    (tmp_path / "app.py").write_text(
        "def hello():\n    return 'hello'",
        encoding="utf-8",
    )

    (tmp_path / "README.md").write_text(
        "# Example Project",
        encoding="utf-8",
    )

    workspace = Workspace(tmp_path)

    summary = workspace.build_summary()

    print("\nWorkspace summary:")
    print(summary)

    assert "app.py" in summary
    assert "README.md" in summary
    assert "def hello()" in summary
    assert "# Example Project" in summary

def test_workspace_builds_file_tree(tmp_path: Path):
    (tmp_path / "app.py").write_text(
        "print('hello')",
        encoding="utf-8",
    )

    src_dir = tmp_path / "src"
    src_dir.mkdir()

    (src_dir / "service.py").write_text(
        "class Service:\n    pass",
        encoding="utf-8",
    )

    workspace = Workspace(tmp_path)

    tree = workspace.build_file_tree()

    print("\nRepository file tree:")
    print(tree)

    assert "app.py" in tree
    assert "src" in tree
    assert "service.py" in tree

def test_workspace_builds_context_for_selected_files(tmp_path: Path):
    (tmp_path / "app.py").write_text(
        "def hello():\n    return 'hello'",
        encoding="utf-8",
    )

    (tmp_path / "other.py").write_text(
        "print('other')",
        encoding="utf-8",
    )

    workspace = Workspace(tmp_path)

    context = workspace.build_context_for_files(
        [
            "app.py",
            "does-not-exist.py",
        ]
    )

    print("\nFocused context:")
    print(context)

    assert "app.py" in context
    assert "def hello()" in context
    assert "other.py" not in context
    assert "does-not-exist.py" not in context