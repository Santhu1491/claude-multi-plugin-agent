"""AST analysis for Python code."""

import ast
from typing import Any


class ASTAnalyzer:
    """Analyze Python AST for structure and metrics."""

    def analyze(self, tree: ast.AST) -> dict[str, Any]:
        """Perform comprehensive AST analysis."""
        return {
            "functions": self._extract_functions(tree),
            "classes": self._extract_classes(tree),
            "imports": self._extract_imports(tree),
            "complexity": self._calculate_complexity(tree),
            "metrics": self._calculate_metrics(tree)
        }

    def _extract_functions(self, tree: ast.AST) -> list[dict[str, Any]]:
        """Extract all function definitions."""
        functions = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append({
                    "name": node.name,
                    "line": node.lineno,
                    "args": [arg.arg for arg in node.args.args],
                    "decorators": [ast.unparse(d) for d in node.decorator_list],
                    "is_async": isinstance(node, ast.AsyncFunctionDef)
                })
        return functions

    def _extract_classes(self, tree: ast.AST) -> list[dict[str, Any]]:
        """Extract all class definitions."""
        classes = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                classes.append({
                    "name": node.name,
                    "line": node.lineno,
                    "bases": [ast.unparse(base) for base in node.bases],
                    "methods": self._extract_methods(node)
                })
        return classes

    def _extract_methods(self, class_node: ast.ClassDef) -> list[str]:
        """Extract method names from a class."""
        methods = []
        for node in class_node.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                methods.append(node.name)
        return methods

    def _extract_imports(self, tree: ast.AST) -> list[dict[str, Any]]:
        """Extract all import statements."""
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append({
                        "module": alias.name,
                        "alias": alias.asname,
                        "line": node.lineno
                    })
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    imports.append({
                        "module": f"{node.module}.{alias.name}" if node.module else alias.name,
                        "alias": alias.asname,
                        "line": node.lineno,
                        "from": node.module
                    })
        return imports

    def _calculate_complexity(self, tree: ast.AST) -> int:
        """Calculate cyclomatic complexity."""
        complexity = 1
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
        return complexity

    def _calculate_metrics(self, tree: ast.AST) -> dict[str, int]:
        """Calculate code metrics."""
        return {
            "total_lines": self._count_lines(tree),
            "num_functions": len([n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]),
            "num_classes": len([n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]),
            "num_imports": len([n for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom))])
        }

    def _count_lines(self, tree: ast.AST) -> int:
        """Count lines of code."""
        max_line = 0
        for node in ast.walk(tree):
            if hasattr(node, 'lineno'):
                max_line = max(max_line, node.lineno)
        return max_line
