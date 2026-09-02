"""Main agent orchestration."""

from typing import Any

from agent.core import workspace
from agent.core.router import Router
from agent.core.planner import Planner
from agent.core.executor import Executor
from agent.core.context import Context
from agent.core.workspace import Workspace
from agent.core.file_selector import FileSelector
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
        self.file_selector = FileSelector(self.claude)

        self.router = Router()
        self.planner = Planner()
        self.executor = Executor()
        self.executor.register_plugin("python", PythonPlugin())
        self.executor.register_plugin("java", JavaPluginAdapter())

    def process_request(self, request: dict[str, Any]) -> dict[str, Any]:
        """Process a user request through the agent pipeline."""

        # Store original request in context
        self.context.add_message(request)

        workspace = Workspace(".")

        file_tree = workspace.build_file_tree()

        selected_files = self.file_selector.select_files(
            request,
            file_tree,
        )

        workspace_context = workspace.build_context_for_files(
            selected_files,
            max_chars_per_file=3000,
        )

        claude_analysis = self._analyze_with_claude(
            request,
            workspace_context,
        )

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
    workspace_summary: str,
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

        Repository context:
        {workspace_summary}

        Use the repository context to understand the existing project structure
        and identify relevant files that may need to be created or modified.

        Return:

        Technology: <python or java>

        Understanding:
        <short explanation>

        Relevant Files:
        List the exact repository-relative paths of existing files that are
        relevant to this request. Prefer existing files from the repository
        context. Do not invent paths unless a new file is genuinely required.
        
        - <repository-relative path>

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