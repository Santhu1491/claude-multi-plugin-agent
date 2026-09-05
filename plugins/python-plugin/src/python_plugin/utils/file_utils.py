"""File utility functions."""

from pathlib import Path
from typing import Any


class FileUtils:
    """Utilities for file operations."""

    @staticmethod
    def ensure_directory(path: str) -> None:
        """Ensure a directory exists."""
        Path(path).mkdir(parents=True, exist_ok=True)

    @staticmethod
    def find_python_files(root: str, exclude_patterns: list[str] | None = None) -> list[Path]:
        """Find all Python files in a directory."""
        exclude_patterns = exclude_patterns or ['__pycache__', '.venv', 'venv', '.git']
        root_path = Path(root)
        
        python_files = []
        for py_file in root_path.rglob("*.py"):
            if not any(pattern in str(py_file) for pattern in exclude_patterns):
                python_files.append(py_file)
        
        return python_files

    @staticmethod
    def get_relative_path(file_path: str, root: str) -> str:
        """Get relative path from root."""
        return str(Path(file_path).relative_to(root))

    @staticmethod
    def read_file_safe(file_path: str) -> str | None:
        """Safely read a file, returning None on error."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except (OSError, UnicodeError):
            return None

    @staticmethod
    def get_file_stats(file_path: str) -> dict[str, Any]:
        """Get file statistics."""
        path = Path(file_path)
        
        if not path.exists():
            return {"error": "File not found"}
        
        stat = path.stat()
        return {
            "size": stat.st_size,
            "created": stat.st_ctime,
            "modified": stat.st_mtime,
            "is_file": path.is_file(),
            "is_dir": path.is_dir()
        }
