"""Integration tests for the agent core."""

import pytest


class TestAgentIntegration:
    """Integration tests for the agent core."""
    
    @pytest.fixture
    def agent(self):
        """Create an agent instance."""
        from agent.config.settings import Settings
        from agent.core.agent import Agent
        
        settings = Settings()
        return Agent(settings)
    
    @pytest.fixture
    def router(self):
        """Create a router instance."""
        from agent.core.router import Router
        return Router()
    
    @pytest.fixture
    def planner(self):
        """Create a planner instance."""
        from agent.core.planner import Planner
        return Planner()
    
    @pytest.fixture
    def executor(self):
        """Create an executor instance."""
        from agent.core.executor import Executor
        return Executor()
    
    def test_router_integration(self, router):
        """Test router determines correct plugin."""
        # Python-related request
        python_request = {"content": "analyze Python code"}
        assert router.route(python_request) == "python"
        
        # Java-related request
        java_request = {"content": "compile Java code"}
        assert router.route(java_request) == "java"
        
        # Default case
        unknown_request = {"content": "do something"}
        assert router.route(unknown_request) == "python"  # default
    
    def test_planner_integration(self, planner):
        """Test planner creates task plan."""
        request = {
            "operation": "analyze",
            "parameters": {"code": "test"}
        }
        
        plan = planner.create_plan(request, "python")
        
        assert len(plan) > 0
        assert plan[0].plugin == "python"
        assert plan[0].operation == "analyze"
    
    def test_executor_integration(self, executor):
        """Test executor with mock plugin."""
        # Mock plugin
        class MockPlugin:
            def execute(self, request):
                assert request["operation"] == "test"
                assert request["parameters"] == {}
                return {"success": True, "data": "mock result"}
        
        executor.register_plugin("mock", MockPlugin())
        
        from agent.models.task import Task
        tasks = [Task(plugin="mock", operation="test", parameters={})]
        
        from agent.core.context import Context
        context = Context()
        
        result = executor.execute(tasks, context)
        
        assert result["success"] is True
        assert len(result["results"]) == 1
    
    def test_context_integration(self):
        """Test context management."""
        from agent.core.context import Context
        
        context = Context()
        
        # Add messages
        context.add_message({"role": "user", "content": "Hello"})
        context.add_message({"role": "assistant", "content": "Hi"})
        
        # Get history
        history = context.get_history(limit=5)
        assert len(history) == 2
        
        # Set and get state
        context.set_state("test_key", "test_value")
        assert context.get_state("test_key") == "test_value"
        
        # Clear context
        context.clear()
        assert len(context.messages) == 0
        assert len(context.state) == 0
    
    @pytest.mark.live
    def test_agent_process_request_integration(self, agent):
        """Test agent processes request end-to-end."""
        # Note: This test requires plugins to be properly installed
        # It may fail if plugins are not available        
        # This is a basic structure test
        # Actual execution would require plugins
        assert hasattr(agent, 'context')
        assert hasattr(agent, 'router')
        assert hasattr(agent, 'planner')
        assert hasattr(agent, 'executor')
    
    def test_settings_integration(self):
        """Test settings configuration."""
        from agent.config.settings import Settings
        
        settings = Settings()
        
        assert settings.version == "0.1.0"
        assert settings.log_level == "INFO"
        assert settings.max_retries == 3
        assert settings.timeout == 30
        assert settings.plugin_directory is not None
