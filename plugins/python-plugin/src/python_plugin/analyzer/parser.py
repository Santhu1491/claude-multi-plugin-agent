"""Python code parser."""

import ast
from typing import Any


class Parser:
    """Parse Python source code into AST."""

    def parse(self, code: str) -> ast.AST:
        """Parse Python code string into an AST."""
        try:
            return ast.parse(code)
        except SyntaxError as e:
            raise ValueError(f"Syntax error in code: {e}")

    def parse_file(self, file_path: str) -> ast.AST:
        """Parse a Python file into an AST."""
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        return self.parse(code)

    def unparse(self, tree: ast.AST) -> str:
        """Convert AST back to Python code."""
        return ast.unparse(tree)

    def validate_syntax(self, code: str) -> dict[str, Any]:
        """Validate Python syntax."""
        try:
            ast.parse(code)
            return {"valid": True, "errors": []}
        except SyntaxError as e:
            return {
                "valid": False,
                "errors": [{
                    "line": e.lineno,
                    "offset": e.offset,
                    "message": e.msg
                }]
            }
