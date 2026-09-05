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
        """Create and switch to a new branch."""

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