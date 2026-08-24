"""Code writing and modification utilities."""

from pathlib import Path
from typing import Any


class CodeWriter:
    """Write and modify Python code files."""

    def write_file(self, file_path: str, content: str) -> dict[str, Any]:
        """Write content to a Python file."""
        try:
            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return {
                "success": True,
                "path": str(path),
                "bytes_written": len(content)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def append_to_file(self, file_path: str, content: str) -> dict[str, Any]:
        """Append content to a file."""
        try:
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write(content)
            
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def insert_at_line(self, file_path: str, line_num: int, content: str) -> dict[str, Any]:
        """Insert content at a specific line."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            lines.insert(line_num - 1, content + '\n')
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def replace_in_file(self, file_path: str, old: str, new: str) -> dict[str, Any]:
        """Replace text in a file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            modified = content.replace(old, new)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(modified)
            
            return {
                "success": True,
                "replacements": content.count(old)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
