"""Tests for the executor module."""

from python_plugin.execution.executor import Executor
from python_plugin.execution.sandbox import Sandbox


def test_executor_simple_code():
    """Test executing simple code."""
    executor = Executor()
    result = executor.execute("x = 1 + 2")
    
    assert result["success"] is True
    assert result["error"] is None


def test_executor_with_output():
    """Test executing code with output."""
    executor = Executor()
    result = executor.execute("print('Hello, World!')")
    
    assert result["success"] is True
    assert "Hello, World!" in result["output"]


def test_executor_with_error():
    """Test executing code with error."""
    executor = Executor()
    result = executor.execute("x = 1 / 0")
    
    assert result["success"] is False
    assert result["error"] is not None
    assert "ZeroDivisionError" in result["error"]


def test_sandbox_restricted_execution():
    """Test sandbox restricts dangerous operations."""
    sandbox = Sandbox()
    
    # Should work - allowed operations
    result = sandbox.execute("x = sum([1, 2, 3])")
    assert result["success"] is True
    
    # Should fail - file operations not in allowed builtins
    result = sandbox.execute("open('test.txt', 'w')")
    assert result["success"] is False


def test_sandbox_evaluate():
    """Test sandbox expression evaluation."""
    sandbox = Sandbox()
    
    result = sandbox.evaluate("2 + 2")
    assert result["success"] is True
    assert result["value"] == 4
    
    result = sandbox.evaluate("sum([1, 2, 3, 4])")
    assert result["success"] is True
    assert result["value"] == 10
