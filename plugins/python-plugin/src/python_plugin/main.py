"""Main Python plugin interface."""

from typing import Any

from python_plugin.analyzer.ast_analyzer import ASTAnalyzer
from python_plugin.analyzer.dependency_analyzer import DependencyAnalyzer
from python_plugin.analyzer.parser import Parser
from python_plugin.execution.executor import Executor
from python_plugin.execution.sandbox import Sandbox
from python_plugin.tools.code_reader import CodeReader
from python_plugin.tools.code_search import CodeSearch
from python_plugin.tools.code_writer import CodeWriter
from python_plugin.tools.linter import Linter
from python_plugin.tools.test_runner import TestRunner


class PythonPlugin:
    """Main plugin interface for Python code operations."""

    name = "python"
    version = "0.1.0"
    description = "Python code analysis and execution plugin"

    def __init__(self) -> None:
        """Initialize the Python plugin with all components."""
        # Analyzer components
        self.parser = Parser()
        self.ast_analyzer = ASTAnalyzer()
        self.dependency_analyzer = DependencyAnalyzer()
        
        # Tool components
        self.code_search = CodeSearch()
        self.code_reader = CodeReader()
        self.code_writer = CodeWriter()
        self.test_runner = TestRunner()
        self.linter = Linter()
        
        # Execution components
        self.executor = Executor()
        self.sandbox = Sandbox()

    def execute(self, request: dict[str, Any]) -> dict[str, Any]:
        """Execute a plugin request."""
        operation = request.get("operation", "")
        parameters = request.get("parameters", {})

        try:
            if operation == "parse":
                return self._parse(parameters)
            elif operation == "analyze":
                return self._analyze(parameters)
            elif operation == "search":
                return self._search(parameters)
            elif operation == "execute":
                return self._execute(parameters)
            elif operation == "test":
                return self._test(parameters)
            elif operation == "lint":
                return self._lint(parameters)
            else:
                return {
                    "success": False,
                    "error": f"Unknown operation: {operation}"
                }
        except Exception as e:  # noqa: BLE001
            return {
                "success": False,
                "error": str(e)
            }

    def _parse(self, params: dict[str, Any]) -> dict[str, Any]:
        """Parse Python code."""
        code = params.get("code", "")
        result = self.parser.parse(code)
        return {"success": True, "data": result}

    def _analyze(self, params: dict[str, Any]) -> dict[str, Any]:
        """Analyze Python code structure."""
        code = params.get("code", "")
        ast_tree = self.parser.parse(code)
        analysis = self.ast_analyzer.analyze(ast_tree)
        return {"success": True, "data": analysis}

    def _search(self, params: dict[str, Any]) -> dict[str, Any]:
        """Search for code patterns."""
        query = params.get("query", "")
        path = params.get("path", ".")
        results = self.code_search.search(query, path)
        return {"success": True, "data": results}

    def _execute(self, params: dict[str, Any]) -> dict[str, Any]:
        """Execute Python code safely."""
        code = params.get("code", "")
        result = self.sandbox.execute(code)
        return {"success": True, "data": result}

    def _test(self, params: dict[str, Any]) -> dict[str, Any]:
        """Run tests."""
        path = params.get("path", "tests")
        results = self.test_runner.run(path)
        return {"success": True, "data": results}

    def _lint(self, params: dict[str, Any]) -> dict[str, Any]:
        """Lint Python code."""
        code = params.get("code", "")
        issues = self.linter.lint(code)
        return {"success": True, "data": issues}
