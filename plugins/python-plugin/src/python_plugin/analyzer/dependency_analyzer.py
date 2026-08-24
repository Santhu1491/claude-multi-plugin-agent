"""Dependency analysis for Python projects."""

import ast
from pathlib import Path
from typing import Any


class DependencyAnalyzer:
    """Analyze dependencies in Python projects."""

    def analyze_file(self, file_path: str) -> dict[str, Any]:
        """Analyze dependencies in a single file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read())
        
        return {
            "file": file_path,
            "imports": self._extract_imports(tree),
            "dependencies": self._categorize_dependencies(tree)
        }

    def analyze_project(self, root_path: str) -> dict[str, Any]:
        """Analyze dependencies across an entire project."""
        root = Path(root_path)
        python_files = list(root.rglob("*.py"))
        
        all_imports = set()
        file_dependencies = {}
        
        for py_file in python_files:
            with open(py_file, 'r', encoding='utf-8') as f:
                try:
                    tree = ast.parse(f.read())
                    imports = self._extract_imports(tree)
                    file_dependencies[str(py_file)] = imports
                    all_imports.update(imp["module"] for imp in imports)
                except SyntaxError:
                    continue
        
        return {
            "root": root_path,
            "files_analyzed": len(python_files),
            "total_imports": len(all_imports),
            "unique_modules": sorted(all_imports),
            "file_dependencies": file_dependencies
        }

    def _extract_imports(self, tree: ast.AST) -> list[dict[str, Any]]:
        """Extract import information from AST."""
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append({
                        "module": alias.name,
                        "alias": alias.asname,
                        "type": "import"
                    })
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    imports.append({
                        "module": f"{module}.{alias.name}" if module else alias.name,
                        "from": module,
                        "alias": alias.asname,
                        "type": "from_import"
                    })
        return imports

    def _categorize_dependencies(self, tree: ast.AST) -> dict[str, list[str]]:
        """Categorize dependencies into standard lib, third-party, and local."""
        imports = self._extract_imports(tree)
        
        stdlib_modules = {'os', 'sys', 'ast', 'pathlib', 'typing', 'dataclasses', 
                         'json', 'datetime', 're', 'collections', 'itertools'}
        
        categorized = {
            "standard_library": [],
            "third_party": [],
            "local": []
        }
        
        for imp in imports:
            module = imp["module"].split(".")[0]
            if module in stdlib_modules:
                categorized["standard_library"].append(module)
            elif module.startswith("."):
                categorized["local"].append(module)
            else:
                categorized["third_party"].append(module)
        
        return categorized
