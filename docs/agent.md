# Agent Core

The agent core provides the central orchestration and execution layer for the multi-plugin system.

## Components

### Agent

The main orchestrator that coordinates all components:

```python
from agent.core.agent import Agent
from agent.config.settings import Settings

settings = Settings()
agent = Agent(settings)

# Process a request
response = agent.process_request({
    "content": "analyze this Python code",
    "operation": "analyze",
    "parameters": {"code": "def hello(): pass"}
})
```

### Router

Determines which plugin should handle a request:

```python
from agent.core.router import Router

router = Router()
plugin_name = router.route({"content": "parse Python code"})
# Returns: "python"
```

The router uses keyword matching to determine the appropriate plugin:

- **Python keywords**: analyze, parse, python, code
- **Java keywords**: compile, maven, java, spring

### Planner

Decomposes requests into executable tasks:

```python
from agent.core.planner import Planner

planner = Planner()
tasks = planner.create_plan(request, "python")
# Returns: list of Task objects
```

### Executor

Executes planned tasks using registered plugins:

```python
from agent.core.executor import Executor

executor = Executor()
executor.register_plugin("python", python_plugin)
executor.register_plugin("java", java_plugin)

result = executor.execute(tasks, context)
```

### Context

Maintains conversation history and execution state:

```python
from agent.core.context import Context

context = Context()
context.add_message({"role": "user", "content": "Hello"})
context.set_state("current_plugin", "python")

history = context.get_history(limit=10)
plugin = context.get_state("current_plugin")
```

## Data Models

### Request

```python
from agent.models.request import Request

request = Request(
    content="Analyze this code",
    operation="analyze",
    parameters={"code": "..."},
    context={}
)
```

### Response

```python
from agent.models.response import Response

response = Response(
    success=True,
    data={"analysis": "..."},
    error=None,
    metadata={"duration": 0.5}
)
```

### Task

```python
from agent.models.task import Task

task = Task(
    plugin="python",
    operation="analyze",
    parameters={"code": "..."},
    priority=1,
    dependencies=[]
)
```

## Configuration

Settings are loaded from environment variables and can be configured:

```python
from agent.config.settings import Settings

settings = Settings()
settings.api_key = "your-api-key"
settings.plugin_directory = Path("plugins")
settings.log_level = "DEBUG"
settings.max_retries = 5
settings.timeout = 60

if settings.validate():
    print("Configuration valid")
```

## Extensibility

### Adding a New Plugin

1. Create plugin in `plugins/` directory
2. Implement the plugin interface
3. Register with executor:

```python
executor.register_plugin("new_plugin", new_plugin_instance)
```

4. Update router keywords:

```python
router.register_route("new_plugin", ["keyword1", "keyword2"])
```

### Custom Planning

Extend the Planner class to implement custom task decomposition:

```python
class CustomPlanner(Planner):
    def create_plan(self, request, plugin_name):
        # Custom planning logic
        return tasks
```

### State Management

Use Context to maintain custom state:

```python
context.set_state("custom_key", value)
value = context.get_state("custom_key", default=None)
```
