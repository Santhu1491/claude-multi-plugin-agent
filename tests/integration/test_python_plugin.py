"""Integration tests for Python plugin."""

import pytest
from pathlib import Path


class TestPythonPluginIntegration:
    """Integration tests for the Python plugin."""
    
    @pytest.fixture
    def plugin(self):
        """Create a Python plugin instance."""
        # Import here to avoid issues if plugin not installed
        from python_plugin.main import PythonPlugin
        return PythonPlugin()
    
    def test_parse_integration(self, plugin):
        """Test parsing Python code end-to-end."""
        code = """
def calculate(a, b):
    return a + b

class Calculator:
    def add(self, x, y):
        return x + y
"""
        
        result = plugin.execute({
            "operation": "parse",
            "parameters": {"code": code}
        })
        
        assert result["success"] is True
        assert "data" in result
    
    def test_analyze_integration(self, plugin):
        """Test analyzing Python code end-to-end."""
        code = """
import os
from pathlib import Path

def function1():
    pass

class MyClass:
    def method1(self):
        pass
"""
        
        result = plugin.execute({
            "operation": "analyze",
            "parameters": {"code": code}
        })
        
        assert result["success"] is True
        data = result["data"]
        assert "functions" in data
        assert "classes" in data
        assert "imports" in data
    
    def test_execute_integration(self, plugin):
        """Test executing Python code end-to-end."""
        code = "print('Hello from integration test')"
        
        result = plugin.execute({
            "operation": "execute",
            "parameters": {"code": code}
        })
        
        assert result["success"] is True
        assert "data" in result
    
    def test_lint_integration(self, plugin):
        """Test linting Python code end-to-end."""
        code = """
def my_function():
    x=1+2
    this_is_a_very_long_variable_name_that_exceeds_the_maximum_line_length_and_should_trigger_a_warning = 1
"""
        
        result = plugin.execute({
            "operation": "lint",
            "parameters": {"code": code}
        })
        
        assert result["success"] is True
        assert "data" in result
    
    def test_invalid_operation(self, plugin):
        """Test handling of invalid operation."""
        result = plugin.execute({
            "operation": "invalid_operation",
            "parameters": {}
        })
        
        assert result["success"] is False
        assert "error" in result
