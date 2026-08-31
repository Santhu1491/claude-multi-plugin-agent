"""Repository workspace inspection utilities."""

from pathlib import Path
from typing import Iterable


class Workspace:
    """Provides safe read-only access to a source repository."""

    DEFAULT_IGNORED_DIRS = {
        ".git",
        ".idea",
        ".vscode",
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        ".venv",
        "venv",
        "node_modules",
        "target",
        "build",
        "dist",
        "*.egg-info",
    }

    def __init__(self, root_path: str | Path) -> None:
        self.root = Path(root_path).resolve()

        if not self.root.exists():
            raise ValueError(f"Workspace does not exist: {self.root}")

        if not self.root.is_dir():
            raise ValueError(f"Workspace is not a directory: {self.root}")

    def list_files(self) -> list[str]:
        """Return repository files using paths relative to the workspace root."""

        files: list[str] = []

        for path in self.root.rglob("*"):
            if not path.is_file():
                continue

            if self._should_ignore(path):
                continue

            files.append(str(path.relative_to(self.root)))

        return sorted(files)

    def read_file(self, relative_path: str) -> str:
        """Read a UTF-8 text file from the workspace."""

        file_path = (self.root / relative_path).resolve()

        if not self._is_inside_workspace(file_path):
            raise ValueError("Attempted to access a file outside the workspace.")

        if not file_path.exists():
            raise FileNotFoundError(relative_path)

        if not file_path.is_file():
            raise ValueError(f"Not a file: {relative_path}")

        return file_path.read_text(
            encoding="utf-8",
            errors="replace",
        )

    def _should_ignore(self, path: Path) -> bool:
        relative_parts: Iterable[str] = path.relative_to(self.root).parts

        for part in relative_parts:
            if part in self.DEFAULT_IGNORED_DIRS:
                return True

            if part.endswith(".egg-info"):
                return True

        return False

    def _is_inside_workspace(self, path: Path) -> bool:
        try:
            path.relative_to(self.root)
            return True
        except ValueError:
            return False

    def build_summary(self, max_files: int = 100, max_chars_per_file: int = 2000) -> str:
        """Build a compact textual summary of the repository."""

        files = self.list_files()

        lines = [
            f"Workspace: {self.root}",
            f"Total files discovered: {len(files)}",
            "",
            "Files:",
        ]

        selected_files = files[:max_files]

        for relative_path in selected_files:
            lines.append(f"- {relative_path}")

        if len(files) > max_files:
            lines.append(
                f"- ... {len(files) - max_files} additional files omitted"
            )

        lines.append("")
        lines.append("Relevant file previews:")

        for relative_path in selected_files:
            if not self._is_text_candidate(relative_path):
                continue

            try:
                content = self.read_file(relative_path)
            except (OSError, ValueError):
                continue

            preview = content[:max_chars_per_file]

            lines.append("")
            lines.append(f"--- {relative_path} ---")
            lines.append(preview)

            if len(content) > max_chars_per_file:
                lines.append("[content truncated]")

        return "\n".join(lines)


    def _is_text_candidate(self, relative_path: str) -> bool:
        """Return whether a file is useful as source-code context."""
    
        allowed_suffixes = {
            ".py",
            ".java",
            ".xml",
            ".toml",
            ".yaml",
            ".yml",
            ".json",
            ".md",
            ".txt",
            ".properties",
        }
    
        path = Path(relative_path)
    
        return path.suffix.lower() in allowed_suffixes