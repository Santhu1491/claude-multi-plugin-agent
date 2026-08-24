# Claude Multi-Plugin Agent

A sophisticated multi-plugin agent system that orchestrates Python and Java plugins for code analysis, manipulation, and execution tasks.

## Overview

The Claude Multi-Plugin Agent is a modular architecture that enables AI-powered code operations across multiple programming languages. The system features:

- **Agent Core**: Central orchestration layer with routing, planning, and execution
- **Python Plugin**: Comprehensive Python code analysis and execution
- **Java Plugin**: Java code analysis and compilation support
- **Extensible Architecture**: Easy to add new language plugins

## Features

### Agent Core
- **Smart Routing**: Automatically determines which plugin to use
- **Task Planning**: Decomposes complex requests into executable tasks
- **State Management**: Maintains conversation context and execution state
- **Plugin Orchestration**: Coordinates multiple plugins seamlessly

### Python Plugin
- AST parsing and analysis
- Code search and navigation
- Safe code execution in sandboxed environments
- Test runner integration
- Code linting and quality checks

### Java Plugin
- Java code parsing and analysis
- Dependency analysis
- Code compilation and execution
- JUnit test integration
- Code quality checks

## Quick Start

### Prerequisites
- Python 3.10 or higher
- Java 17 or higher
- Maven 3.6+

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/claude-multi-plugin-agent.git
cd claude-multi-plugin-agent

# Run setup script
bash scripts/setup.sh

# Configure API key
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### Usage

```bash
# Run the agent
python agent/main.py

# Or use the convenience script
bash scripts/run_agent.sh
```

## Project Structure

```
claude-multi-plugin-agent/
├── agent/              # Agent core orchestration
│   ├── core/          # Router, planner, executor
│   ├── models/        # Data models
│   └── config/        # Configuration
├── plugins/           # Plugin implementations
│   ├── python-plugin/ # Python analysis & execution
│   └── java-plugin/   # Java analysis & execution
├── examples/          # Sample code for testing
├── docs/              # Documentation
├── tests/             # Integration tests
└── scripts/           # Utility scripts
```

## Documentation

- [Architecture](docs/architecture.md) - System design and components
- [Agent Core](docs/agent.md) - Agent core documentation
- [Python Plugin](docs/python-plugin.md) - Python plugin guide
- [Java Plugin](docs/java-plugin.md) - Java plugin guide
- [Development](docs/development.md) - Development guide

## Development

### Setup Development Environment

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Install plugins
cd plugins/python-plugin && pip install -e ".[dev]" && cd ../..
cd plugins/java-plugin && mvn clean install && cd ../..
```

### Running Tests

```bash
# Python tests
pytest

# Java tests
cd plugins/java-plugin && mvn test && cd ../..

# Integration tests
pytest tests/integration/
```

## Examples

See the [examples/](examples/) directory for sample code:

- **Python**: calculator.py, data_processor.py, api_client.py
- **Java**: Calculator.java, DataProcessor.java, ApiClient.java

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Run all tests and quality checks
5. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) for details

## Architecture

The system uses a layered architecture:

1. **User Request** → Router (determines plugin)
2. **Router** → Planner (creates task plan)
3. **Planner** → Executor (executes tasks)
4. **Executor** → Plugin (performs operations)
5. **Plugin** → Response (returns results)

Each plugin is independent and implements a standard interface, making it easy to add support for new languages.

## Roadmap

- [ ] TypeScript plugin support
- [ ] Go plugin support
- [ ] Enhanced code refactoring capabilities
- [ ] Multi-file operation support
- [ ] Real-time collaboration features

## Support

For questions and support, please open an issue on GitHub.
