# Python Plugin

Python code analysis and execution plugin for the Claude multi-plugin agent.

## Features

- **Code Analysis**: Parse and analyze Python code structure
- **AST Analysis**: Deep analysis of Abstract Syntax Trees
- **Dependency Analysis**: Track imports and dependencies
- **Code Search**: Search through Python codebases
- **Code Execution**: Safe execution in sandboxed environments
- **Testing**: Run and analyze test suites
- **Linting**: Code quality checks

## Installation

```bash
pip install -e .
```

## Usage

```python
from python_plugin import PythonPlugin

plugin = PythonPlugin()
result = plugin.analyze_code("path/to/file.py")
```

## Development

```bash
pip install -e ".[dev]"
pytest
```
