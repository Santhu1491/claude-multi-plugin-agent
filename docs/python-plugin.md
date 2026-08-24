# Python Plugin

The Python plugin provides comprehensive code analysis and execution capabilities for Python code.

## Features

### Code Analysis

- **Parser**: Parse Python source code into AST
- **AST Analyzer**: Extract functions, classes, imports, and calculate complexity
- **Dependency Analyzer**: Track imports and dependencies across projects

### Code Tools

- **Code Search**: Search for patterns and symbols in Python files
- **Code Reader**: Read files and extract information
- **Code Writer**: Write and modify Python files
- **Test Runner**: Execute pytest tests
- **Linter**: Check code quality and style

### Code Execution

- **Executor**: Run Python code and capture output
- **Sandbox**: Execute code in a restricted environment

## Usage

### Parse Code

```python
from python_plugin import PythonPlugin

plugin = PythonPlugin()
result = plugin.execute({
    "operation": "parse",
    "parameters": {
        "code": "def hello(): pass"
    }
})
```

### Analyze Code

```python
result = plugin.execute({
    "operation": "analyze",
    "parameters": {
        "code": "class MyClass:\n    def method(self): pass"
    }
})

# Returns: functions, classes, imports, complexity, metrics
```

### Search Code

```python
result = plugin.execute({
    "operation": "search",
    "parameters": {
        "query": "def.*calculate",
        "path": "src/"
    }
})
```

### Execute Code

```python
result = plugin.execute({
    "operation": "execute",
    "parameters": {
        "code": "print('Hello, World!')"
    }
})
```

### Run Tests

```python
result = plugin.execute({
    "operation": "test",
    "parameters": {
        "path": "tests/"
    }
})
```

### Lint Code

```python
result = plugin.execute({
    "operation": "lint",
    "parameters": {
        "code": "def function_with_long_name():\n    x=1+2"
    }
})
```

## API Reference

See the [Python Plugin API documentation](python-plugin-api.md) for detailed API reference.

## Development

### Setup

```bash
cd plugins/python-plugin
pip install -e ".[dev]"
```

### Run Tests

```bash
pytest
```

### Type Checking

```bash
mypy src/
```

### Linting

```bash
ruff check src/
black src/
```
