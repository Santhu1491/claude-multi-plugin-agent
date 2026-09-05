"""Local Git repository operations."""

import subprocess
from pathlib import Path


class GitClient:
    """Provides safe local Git operations for the agent."""

    def __init__(self, repo_path: str | Path) -> None:
        self.repo_path = Path(repo_path).resolve()

        if not (self.repo_path / ".git").exists():
            raise ValueError(
                f"Not a Git repository: {self.repo_path}"
            )

    def _run(self, *args: str) -> str:
        result = subprocess.run(
            ["git", *args],
            cwd=self.repo_path,
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            raise RuntimeError(
                result.stderr.strip()
                or result.stdout.strip()
                or "Git command failed."
            )

        return result.stdout.strip()

    def current_branch(self) -> str:
        """Return the active Git branch."""

        return self._run(
            "branch",
            "--show-current",
        )

    def status(self) -> str:
        """Return the short Git working-tree status."""

        return self._run(
            "status",
            "--short",
        )

    def create_branch(self, branch_name: str) -> str:
        """Create and switch to a branch safely."""

        if self.branch_exists(branch_name):
            self._run(
                "switch",
                branch_name,
            )
        else:
            self._run(
                "switch",
                "-c",
                branch_name,
            )

        return self.current_branch()

    def stage_all(self) -> None:
        """Stage all repository changes."""

        self._run(
            "add",
            ".",
        )

    def commit(self, message: str) -> str:
        """Create a Git commit and return its hash."""
    
        if not message.strip():
            raise ValueError("Commit message cannot be empty.")
    
        if not self.has_changes():
            raise RuntimeError(
                "No repository changes available to commit."
            )
    
        self.stage_all()
    
        self._run(
            "commit",
            "-m",
            message,
        )
    
        return self._run(
            "rev-parse",
            "HEAD",
        )

    def remote_url(self, remote_name: str = "origin") -> str:
        """Return the URL configured for a Git remote."""
    
        return self._run(
            "remote",
            "get-url",
            remote_name,
        )
    
    
    def push(
        self,
        branch_name: str | None = None,
        remote_name: str = "origin",
    ) -> None:
        """Push a branch to the configured remote."""
    
        branch = branch_name or self.current_branch()
    
        self._run(
            "push",
            "-u",
            remote_name,
            branch,
        )

    def branch_exists(self, branch_name: str) -> bool:
        """Return True if a local branch already exists."""

        result = subprocess.run(
            [
                "git",
                "branch",
                "--list",
                branch_name,
            ],
            cwd=self.repo_path,
            capture_output=True,
            text=True,
            check=False,
        )

        return bool(result.stdout.strip())


    def has_changes(self) -> bool:
        """Return True if the working tree has uncommitted changes."""

        return bool(self.status().strip())


    def ensure_safe_branch(self) -> None:
        """Prevent publishing directly from protected branches."""

        branch = self.current_branch()

        if branch in {"main", "master"}:
            raise RuntimeError(
                f"Publishing directly from protected branch "
                f"'{branch}' is not allowed."
            )