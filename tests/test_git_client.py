import subprocess
from pathlib import Path

from agent.integrations.git_client import GitClient


def run_git(repo: Path, *args: str):
    subprocess.run(
        ["git", *args],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    )

def run_git_capture(
    repo: Path,
    *args: str,
) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    )

    return result.stdout.strip()


def create_test_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()

    run_git(repo, "init")

    run_git(repo, "config", "user.email", "test@example.com")
    run_git(repo, "config", "user.name", "Test User")

    file_path = repo / "README.md"
    file_path.write_text(
        "# Test\n",
        encoding="utf-8",
    )

    run_git(repo, "add", ".")
    run_git(repo, "commit", "-m", "Initial commit")

    return repo


def test_git_client_current_branch(tmp_path: Path):
    repo = create_test_repo(tmp_path)

    client = GitClient(repo)

    branch = client.current_branch()

    assert branch


def test_git_client_status(tmp_path: Path):
    repo = create_test_repo(tmp_path)

    client = GitClient(repo)

    (repo / "app.py").write_text(
        "print('hello')\n",
        encoding="utf-8",
    )

    status = client.status()

    assert "app.py" in status


def test_git_client_create_branch(tmp_path: Path):
    repo = create_test_repo(tmp_path)

    client = GitClient(repo)

    branch = client.create_branch(
        "feature/test-agent"
    )

    assert branch == "feature/test-agent"

def test_git_client_stage_all(tmp_path: Path):
    repo = create_test_repo(tmp_path)

    client = GitClient(repo)

    (repo / "app.py").write_text(
        "print('hello')\n",
        encoding="utf-8",
    )

    client.stage_all()

    staged = run_git_capture(
        repo,
        "diff",
        "--cached",
        "--name-only",
    )

    assert "app.py" in staged


def test_git_client_commit(tmp_path: Path):
    repo = create_test_repo(tmp_path)

    client = GitClient(repo)

    (repo / "app.py").write_text(
        "print('hello')\n",
        encoding="utf-8",
    )

    client.stage_all()

    commit_hash = client.commit(
        "feat: add app"
    )

    assert len(commit_hash) >= 7

    message = run_git_capture(
        repo,
        "log",
        "-1",
        "--pretty=%B",
    )

    assert "feat: add app" in message

def test_git_client_remote_url(tmp_path: Path):
    repo = create_test_repo(tmp_path)

    run_git(
        repo,
        "remote",
        "add",
        "origin",
        "https://example.com/test/repo.git",
    )

    client = GitClient(repo)

    url = client.remote_url()

    assert url == "https://example.com/test/repo.git"

def test_git_client_push(tmp_path: Path):
    remote_repo = tmp_path / "remote.git"

    subprocess.run(
        ["git", "init", "--bare", str(remote_repo)],
        check=True,
        capture_output=True,
        text=True,
    )

    repo = create_test_repo(tmp_path)

    run_git(
        repo,
        "remote",
        "add",
        "origin",
        str(remote_repo),
    )

    client = GitClient(repo)

    client.create_branch("feature/test-push")

    (repo / "app.py").write_text(
        "print('push test')\n",
        encoding="utf-8",
    )

    client.stage_all()
    client.commit("feat: test push")

    client.push()

    branches = subprocess.run(
        [
            "git",
            "--git-dir",
            str(remote_repo),
            "branch",
            "--list",
        ],
        check=True,
        capture_output=True,
        text=True,
    ).stdout

    assert "feature/test-push" in branches

def test_git_client_branch_exists(tmp_path: Path):
    repo = create_test_repo(tmp_path)

    client = GitClient(repo)

    assert client.branch_exists(
        client.current_branch()
    ) is True

    assert client.branch_exists(
        "missing-branch"
    ) is False


def test_git_client_has_changes(tmp_path: Path):
    repo = create_test_repo(tmp_path)

    client = GitClient(repo)

    assert client.has_changes() is False

    (repo / "app.py").write_text(
        "print('hello')\n",
        encoding="utf-8",
    )

    assert client.has_changes() is True


def test_git_client_reuses_existing_branch(tmp_path: Path):
    repo = create_test_repo(tmp_path)

    client = GitClient(repo)

    client.create_branch(
        "feature/existing"
    )

    run_git(
        repo,
        "switch",
        "-",
    )

    branch = client.create_branch(
        "feature/existing"
    )

    assert branch == "feature/existing"


def test_git_client_rejects_empty_commit(tmp_path: Path):
    repo = create_test_repo(tmp_path)

    client = GitClient(repo)

    try:
        client.commit("feat: nothing")
        assert False
    except RuntimeError as exc:
        assert "No repository changes" in str(exc)