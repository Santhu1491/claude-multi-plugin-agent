"""Code linting functionality."""

import ast
from typing import Any


class Linter:
    """Basic Python code linting."""

    def lint(self, code: str) -> list[dict[str, Any]]:
        """Lint Python code for common issues."""
        issues = []
        
        # Check syntax
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            issues.append({
                "type": "syntax_error",
                "line": e.lineno,
                "message": e.msg,
                "severity": "error"
            })
            return issues
        
        # Check for common issues
        issues.extend(self._check_unused_imports(tree))
        issues.extend(self._check_long_lines(code))
        issues.extend(self._check_missing_docstrings(tree))
        
        return issues

    def _check_unused_imports(self, tree: ast.AST) -> list[dict[str, Any]]:
        """Check for potentially unused imports."""
        # This is a simplified check
        issues = []
        imports = []
        names_used = set()
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                for alias in node.names:
                    name = alias.asname or alias.name
                    imports.append((name, node.lineno))
            elif isinstance(node, ast.Name):
                names_used.add(node.id)
        
        for name, line in imports:
            if name not in names_used:
                issues.append({
                    "type": "unused_import",
                    "line": line,
                    "message": f"Import '{name}' appears unused",
                    "severity": "warning"
                })
        
        return issues

    def _check_long_lines(self, code: str, max_length: int = 100) -> list[dict[str, Any]]:
        """Check for lines exceeding maximum length."""
        issues = []
        for line_num, line in enumerate(code.split('\n'), 1):
            if len(line) > max_length:
                issues.append({
                    "type": "line_too_long",
                    "line": line_num,
                    "message": f"Line exceeds {max_length} characters ({len(line)})",
                    "severity": "warning"
                })
        return issues

    def _check_missing_docstrings(self, tree: ast.AST) -> list[dict[str, Any]]:
        """Check for missing docstrings."""
        issues = []
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                if not ast.get_docstring(node):
                    issues.append({
                        "type": "missing_docstring",
                        "line": node.lineno,
                        "message": f"{node.__class__.__name__} '{node.name}' lacks a docstring",
                        "severity": "info"
                    })
        
        return issues
