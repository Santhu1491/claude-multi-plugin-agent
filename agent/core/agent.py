"""Main agent orchestration."""

from typing import Any

from python_plugin.main import PythonPlugin

from agent.config.settings import Settings
from agent.core.change_builder import ChangeBuilder
from agent.core.change_executor import ChangeExecutor
from agent.core.change_planner import ChangePlanner
from agent.core.code_generator import CodeGenerator
from agent.core.context import Context
from agent.core.executor import Executor
from agent.core.file_selector import FileSelector
from agent.core.planner import Planner
from agent.core.router import Router
from agent.core.workspace import Workspace
from agent.core.workspace_writer import WorkspaceWriter
from agent.integrations.claude import ClaudeClient
from agent.integrations.java_plugin_adapter import JavaPluginAdapter


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
        self.executor.register_plugin(
            "python",
            PythonPlugin(),
        )
        self.executor.register_plugin(
            "java",
            JavaPluginAdapter(),
        )

    def process_request(
        self,
        request: dict[str, Any],
    ) -> dict[str, Any]:
        """Process a development request through the complete agent pipeline."""

        # Store original request in context.
        self.context.add_message(request)

        # Inspect the repository.
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

        repository_context = (
            "Repository file tree:\n"
            f"{file_tree}\n\n"
            "Relevant file contents:\n"
            f"{workspace_context}"
        )

        # Ask Claude to analyze the development request.
        claude_analysis = self._analyze_with_claude(
            request,
            repository_context,
        )

        enriched_request = {
            **request,
            "claude_analysis": claude_analysis,
        }

        # Determine which technology plugin should handle the request.
        plugin_name = self.router.route(
            enriched_request,
        )

        # Run the existing plugin execution pipeline.
        plan = self.planner.create_plan(
            enriched_request,
            plugin_name,
        )

        plugin_result = self.executor.execute(
            plan,
            self.context,
        )

        if not plugin_result.get("success", False):
            return {
                "success": False,
                "claude_analysis": claude_analysis,
                "plugin": plugin_name,
                "result": plugin_result,
                "change_result": None,
            }

        # Build the repository modification pipeline.
        writer = WorkspaceWriter(
            workspace.root,
        )

        change_planner = ChangePlanner(
            self.claude,
        )

        code_generator = CodeGenerator(
            self.claude,
        )

        change_builder = ChangeBuilder(
            workspace=workspace,
            generator=code_generator,
        )

        change_executor = ChangeExecutor(
            workspace=workspace,
            writer=writer,
            planner=change_planner,
            builder=change_builder,
            claude=self.claude,
        )

        # Actually generate, write, validate, and heal repository changes.
        change_result = change_executor.execute(
            request=enriched_request,
            repository_context=repository_context,
            technology=plugin_name,
            apply_changes=True,
        )

        changes = change_result.get(
            "changes",
            [],
        )

        healing_results = change_result.get(
            "results",
            [],
        )

        changes_succeeded = (
            bool(changes)
            and bool(healing_results)
            and all(
                self._healing_succeeded(result)
                for result in healing_results
            )
        )

        return {
            "success": (
                plugin_result.get("success", False)
                and changes_succeeded
            ),
            "claude_analysis": claude_analysis,
            "plugin": plugin_name,
            "result": plugin_result,
            "change_result": change_result,
        }

    @staticmethod
    def _healing_succeeded(
        result: Any,
    ) -> bool:
        """Read success from a healing result object or dictionary."""

        if isinstance(result, dict):
            return bool(
                result.get("success", False)
            )

        return bool(
            getattr(
                result,
                "success",
                False,
            )
        )

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