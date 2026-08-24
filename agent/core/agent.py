"""Main agent orchestration."""

from typing import Any
from agent.core.router import Router
from agent.core.planner import Planner
from agent.core.executor import Executor
from agent.core.context import Context
from agent.config.settings import Settings


class Agent:
    """Orchestrates plugin routing, planning, and execution."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.context = Context()
        self.router = Router()
        self.planner = Planner()
        self.executor = Executor()

    def process_request(self, request: dict[str, Any]) -> dict[str, Any]:
        """Process a user request through the agent pipeline."""
        # Update context
        self.context.add_message(request)
        
        # Route to appropriate plugin
        plugin_name = self.router.route(request)
        
        # Plan execution steps
        plan = self.planner.create_plan(request, plugin_name)
        
        # Execute the plan
        result = self.executor.execute(plan, self.context)
        
        return result

    def run(self) -> None:
        """Main agent loop."""
        print("Agent running...")
        # Interactive loop would go here
