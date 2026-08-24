"""Code reading utilities."""

from pathlib import Path
from typing import Any


class CodeReader:
    """Read and extract information from Python code files."""

    def read_file(self, file_path: str) -> str:
        """Read a Python file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    def read_lines(self, file_path: str, start: int, end: int) -> str:
        """Read specific lines from a file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        return ''.join(lines[start-1:end])

    def get_file_info(self, file_path: str) -> dict[str, Any]:
        """Get information about a Python file."""
        path = Path(file_path)
        
        if not path.exists():
            return {"error": "File not found"}
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
        
        return {
            "path": str(path),
            "size": path.stat().st_size,
            "lines": len(lines),
            "is_module": path.name == "__init__.py",
            "name": path.stem
        }

    def list_python_files(self, root_path: str) -> list[str]:
        """List all Python files in a directory."""
        root = Path(root_path)
        return [str(f) for f in root.rglob("*.py")]
