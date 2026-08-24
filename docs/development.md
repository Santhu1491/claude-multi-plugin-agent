# Development Guide

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Java 17 or higher
- Maven 3.6+
- Git

### Clone Repository

```bash
git clone https://github.com/your-org/claude-multi-plugin-agent.git
cd claude-multi-plugin-agent
```

### Setup Environment

#### Python Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (Unix/Mac)
source .venv/bin/activate

# Install dependencies
pip install -e ".[dev]"
```

#### Java Environment

```bash
cd plugins/java-plugin
mvn clean install
```

### Configuration

Create a `.env` file in the project root:

```env
ANTHROPIC_API_KEY=your_api_key_here
```

## Project Structure

```
claude-multi-plugin-agent/
├── agent/              # Agent core
│   ├── core/          # Core components
│   ├── models/        # Data models
│   └── config/        # Configuration
├── plugins/           # Plugin implementations
│   ├── python-plugin/ # Python plugin
│   └── java-plugin/   # Java plugin
├── examples/          # Example code
├── docs/              # Documentation
├── tests/             # Integration tests
└── scripts/           # Utility scripts
```

## Development Workflow

### Python Development

#### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_agent.py

# Run with coverage
pytest --cov=agent --cov-report=html
```

#### Code Quality

```bash
# Format code
black agent/ tests/

# Lint code
ruff check agent/ tests/

# Type checking
mypy agent/
```

#### Python Plugin Development

```bash
cd plugins/python-plugin

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Run specific test
pytest tests/test_parser.py::test_parser_basic_code
```

### Java Development

#### Running Tests

```bash
cd plugins/java-plugin

# Run all tests
mvn test

# Run specific test
mvn test -Dtest=ParserTest

# Generate coverage report
mvn jacoco:report
```

#### Code Quality

```bash
# Compile
mvn compile

# Run checkstyle
mvn checkstyle:check

# Generate JavaDoc
mvn javadoc:javadoc
```

## Adding New Features

### Adding a New Plugin

1. Create plugin directory:
   ```bash
   mkdir -p plugins/my-plugin/src/my_plugin
   ```

2. Implement plugin interface:
   ```python
   class MyPlugin:
       name = "my_plugin"
       
       def execute(self, request):
           # Implementation
           pass
   ```

3. Register plugin in executor:
   ```python
   executor.register_plugin("my_plugin", MyPlugin())
   ```

4. Add routing keywords:
   ```python
   router.register_route("my_plugin", ["keyword1", "keyword2"])
   ```

### Adding New Operations

1. Add operation to plugin's execute method
2. Implement operation handler
3. Add tests
4. Update documentation

## Testing

### Unit Tests

- Test individual components in isolation
- Mock external dependencies
- Use pytest fixtures for setup

### Integration Tests

- Test end-to-end workflows
- Use real plugins but mock external APIs
- Verify component interactions

### Example Test

```python
def test_agent_process_request():
    """Test agent processes request correctly."""
    settings = Settings()
    agent = Agent(settings)
    
    request = {
        "content": "analyze Python code",
        "operation": "analyze",
        "parameters": {"code": "def test(): pass"}
    }
    
    response = agent.process_request(request)
    
    assert response["success"] is True
    assert "data" in response
```

## Documentation

### Writing Documentation

- Use Markdown format
- Include code examples
- Keep it concise and clear
- Update when adding features

### Building Documentation

```bash
# Generate API docs
python -m pydoc -w agent

# For Java
cd plugins/java-plugin
mvn javadoc:javadoc
```

## Debugging

### Python Debugging

Use VS Code debugger or pdb:

```python
import pdb; pdb.set_trace()
```

### Java Debugging

Use IDE debugger or jdb:

```bash
mvn exec:java -Dexec.mainClass="..." -Dexec.args="..." -Dexec.classpathScope=runtime
```

## Performance

### Profiling Python

```bash
python -m cProfile -o output.prof agent/main.py
python -m pstats output.prof
```

### Profiling Java

Use JProfiler or VisualVM for performance analysis.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Run all tests and quality checks
5. Submit pull request

## Troubleshooting

### Common Issues

**Import errors**: Ensure virtual environment is activated and dependencies installed

**Java compilation errors**: Check Java version (17+) and Maven installation

**Test failures**: Check environment variables and test fixtures

**Permission errors**: Verify file permissions and directory access
