"""Tests for the parser module."""

import pytest
from python_plugin.analyzer.parser import Parser


def test_parser_basic_code():
    """Test parsing basic Python code."""
    parser = Parser()
    code = "x = 1 + 2"
    tree = parser.parse(code)
    assert tree is not None


def test_parser_function_definition():
    """Test parsing function definition."""
    parser = Parser()
    code = """
def hello(name):
    return f"Hello, {name}"
"""
    tree = parser.parse(code)
    assert tree is not None


def test_parser_syntax_error():
    """Test parser handles syntax errors."""
    parser = Parser()
    code = "def invalid("
    
    with pytest.raises(ValueError):
        parser.parse(code)


def test_validate_syntax_valid():
    """Test syntax validation with valid code."""
    parser = Parser()
    result = parser.validate_syntax("x = 1")
    assert result["valid"] is True
    assert result["errors"] == []


def test_validate_syntax_invalid():
    """Test syntax validation with invalid code."""
    parser = Parser()
    result = parser.validate_syntax("def invalid(")
    assert result["valid"] is False
    assert len(result["errors"]) > 0
