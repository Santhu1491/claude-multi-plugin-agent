"""Tests for the AST analyzer module."""

import ast
import pytest
from python_plugin.analyzer.ast_analyzer import ASTAnalyzer
from python_plugin.analyzer.parser import Parser


def test_extract_functions():
    """Test extracting function definitions."""
    parser = Parser()
    analyzer = ASTAnalyzer()
    
    code = """
def func1():
    pass

def func2(x, y):
    return x + y
"""
    tree = parser.parse(code)
    analysis = analyzer.analyze(tree)
    
    assert len(analysis["functions"]) == 2
    assert analysis["functions"][0]["name"] == "func1"
    assert analysis["functions"][1]["name"] == "func2"
    assert len(analysis["functions"][1]["args"]) == 2


def test_extract_classes():
    """Test extracting class definitions."""
    parser = Parser()
    analyzer = ASTAnalyzer()
    
    code = """
class MyClass:
    def method1(self):
        pass
    
    def method2(self):
        pass
"""
    tree = parser.parse(code)
    analysis = analyzer.analyze(tree)
    
    assert len(analysis["classes"]) == 1
    assert analysis["classes"][0]["name"] == "MyClass"
    assert len(analysis["classes"][0]["methods"]) == 2


def test_extract_imports():
    """Test extracting import statements."""
    parser = Parser()
    analyzer = ASTAnalyzer()
    
    code = """
import os
import sys
from pathlib import Path
from typing import Any, List
"""
    tree = parser.parse(code)
    analysis = analyzer.analyze(tree)
    
    assert len(analysis["imports"]) == 5


def test_calculate_metrics():
    """Test code metrics calculation."""
    parser = Parser()
    analyzer = ASTAnalyzer()
    
    code = """
def func1():
    pass

class MyClass:
    pass
"""
    tree = parser.parse(code)
    analysis = analyzer.analyze(tree)
    
    metrics = analysis["metrics"]
    assert metrics["num_functions"] == 1
    assert metrics["num_classes"] == 1
