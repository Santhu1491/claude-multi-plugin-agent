"""Safe repository file modification utilities."""

from pathlib import Path
from typing import Any


class WorkspaceWriter:
    """Safely creates and updates files inside a repository workspace."""

    def __init__(self, root_path: str | Path) -> None:
        self.root = Path(root_path).resolve()

        if not self.root.exists():
            raise ValueError(f"Workspace does not exist: {self.root}")

        if not self.root.is_dir():
            raise ValueError(f"Workspace is not a directory: {self.root}")

    def write_file(
        self,
        relative_path: str,
        content: str,
    ) -> dict[str, Any]:
        """Create or replace a text file inside the workspace."""

        file_path = (self.root / relative_path).resolve()

        if not self._is_inside_workspace(file_path):
            raise ValueError(
                "Attempted to write outside the workspace."
            )

        original_content = None

        if file_path.exists():
            if not file_path.is_file():
                raise ValueError(
                    f"Target is not a file: {relative_path}"
                )

            original_content = file_path.read_text(
                encoding="utf-8",
                errors="replace",
            )

        file_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        file_path.write_text(
            content,
            encoding="utf-8",
        )

        return {
            "success": True,
            "path": relative_path,
            "created": original_content is None,
            "original_content": original_content,
            "new_content": content,
        }

    def _is_inside_workspace(
        self,
        path: Path,
    ) -> bool:
        try:
            path.relative_to(self.root)
            return True
        except ValueError:
            return False

    def validate_change_plan(
    self,
    changes: list[dict[str, str]],
    ) -> list[dict[str, str]]:
        """Validate proposed repository changes before writing."""

        validated: list[dict[str, str]] = []

        for change in changes:
            relative_path = change.get("path")
            action = change.get("action")

            if not relative_path:
                raise ValueError("Change path is required.")

            if action not in {"modify", "create"}:
                raise ValueError(
                    f"Unsupported change action: {action}"
                )

            file_path = (
                self.root / relative_path
            ).resolve()

            if not self._is_inside_workspace(file_path):
                raise ValueError(
                    f"Change targets file outside workspace: "
                    f"{relative_path}"
                )

            if action == "modify":
                if not file_path.exists():
                    raise ValueError(
                        f"Cannot modify missing file: "
                        f"{relative_path}"
                    )

                if not file_path.is_file():
                    raise ValueError(
                        f"Modify target is not a file: "
                        f"{relative_path}"
                    )

            if action == "create" and file_path.exists():
                raise ValueError(
                    f"Cannot create existing file: "
                    f"{relative_path}"
                )

            validated.append(change)

        return validated
    def apply_proposed_change(
    self,
    change,
    ) -> dict[str, Any]:
        """Apply a ProposedChange to the workspace."""
    
        return self.write_file(
            change.path,
            change.generated_content,
        )
    
    
    def rollback_proposed_change(
        self,
        change,
    ) -> dict[str, Any]:
        """Rollback an already-applied ProposedChange."""
    
        file_path = (self.root / change.path).resolve()
    
        if not self._is_inside_workspace(file_path):
            raise ValueError(
                "Attempted to rollback outside the workspace."
            )
    
        if change.original_content is None:
            if file_path.exists():
                file_path.unlink()
    
            return {
                "success": True,
                "path": change.path,
                "rolled_back": True,
                "deleted": True,
            }
    
        file_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )
    
        file_path.write_text(
            change.original_content,
            encoding="utf-8",
        )
    
        return {
            "success": True,
            "path": change.path,
            "rolled_back": True,
            "deleted": False,
        }