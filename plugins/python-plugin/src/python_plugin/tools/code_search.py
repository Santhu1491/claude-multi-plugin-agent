"""Code search functionality."""

import re
from pathlib import Path
from typing import Any


class CodeSearch:
    """Search for patterns in Python code."""

    def search(self, query: str, root_path: str = ".") -> list[dict[str, Any]]:
        """Search for a pattern in Python files."""
        root = Path(root_path)
        results = []
        
        for py_file in root.rglob("*.py"):
            matches = self._search_file(py_file, query)
            if matches:
                results.extend(matches)
        
        return results

    def _search_file(self, file_path: Path, query: str) -> list[dict[str, Any]]:
        """Search for pattern in a single file."""
        matches = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    if re.search(query, line, re.IGNORECASE):
                        matches.append({
                            "file": str(file_path),
                            "line": line_num,
                            "content": line.strip()
                        })
        except (OSError, UnicodeError):
            return matches
        
        return matches

    def search_definition(self, symbol: str, root_path: str = ".") -> list[dict[str, Any]]:
        """Search for function or class definitions."""
        pattern = rf"^\s*(def|class)\s+{re.escape(symbol)}\s*[\(\:]"
        return self.search(pattern, root_path)

    def search_usage(self, symbol: str, root_path: str = ".") -> list[dict[str, Any]]:
        """Search for usages of a symbol."""
        pattern = rf"\b{re.escape(symbol)}\b"
        return self.search(pattern, root_path)
