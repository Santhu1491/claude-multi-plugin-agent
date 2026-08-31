"""Main agent orchestration."""

from typing import Any

from agent.core.router import Router
from agent.core.planner import Planner
from agent.core.executor import Executor
from agent.core.context import Context
from agent.config.settings import Settings
from agent.integrations.claude import ClaudeClient
from agent.integrations.java_plugin_adapter import JavaPluginAdapter
from python_plugin.main import PythonPlugin


class Agent:
    """Orchestrates Claude reasoning, plugin routing, planning, and execution."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.context = Context()

        self.claude = ClaudeClient()

        self.router = Router()
        self.planner = Planner()
        self.executor = Executor()
        self.executor.register_plugin("python", PythonPlugin())
        self.executor.register_plugin("java", JavaPluginAdapter())

    def process_request(self, request: dict[str, Any]) -> dict[str, Any]:
        """Process a user request through the agent pipeline."""

        # Store original request in context
        self.context.add_message(request)

        # Ask Claude to understand the requirement
        claude_analysis = self._analyze_with_claude(request)

        # Add Claude's analysis back into the request
        enriched_request = {
            **request,
            "claude_analysis": claude_analysis,
        }

        # Route to appropriate plugin
        plugin_name = self.router.route(enriched_request)

        # Plan execution steps
        plan = self.planner.create_plan(
            enriched_request,
            plugin_name,
        )

        # Execute the plan
        result = self.executor.execute(
            plan,
            self.context,
        )

        return {
            "claude_analysis": claude_analysis,
            "plugin": plugin_name,
            "result": result,
        }

    def _analyze_with_claude(
        self,
        request: dict[str, Any],
    ) -> str:
        """Ask Claude to analyze the development request."""

        prompt = f"""
You are the reasoning engine for a software development agent.

The agent currently supports only two technologies:

1. Python
2. Java

Analyze the following development request.

Request:
{request}

Return:

Technology: <python or java>

Understanding:
<short explanation of what needs to be implemented>

Plan:
1. <step>
2. <step>
3. <step>

Do not generate source code yet.
"""

        return self.claude.generate(prompt)

    def run(self) -> None:
        """Main agent loop."""
        print("Agent running...")