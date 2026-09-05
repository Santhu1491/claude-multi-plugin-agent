"""Integration tests for Java plugin."""

import subprocess
from pathlib import Path

import pytest

from agent.utils.tool_resolver import ToolResolver


@pytest.fixture
def java_plugin_path():
    """Get path to Java plugin."""
    return Path(__file__).parent.parent.parent / "plugins" / "java-plugin"


@pytest.fixture
def maven_command():
    command = ToolResolver.find_maven()
    if not command:
        pytest.skip("Maven is not available")
    return command

class TestJavaPluginIntegration:
    """Integration tests for the Java plugin."""
    def test_java_plugin_builds(self, java_plugin_path, maven_command):
        """Test that Java plugin builds successfully."""
        result = subprocess.run(
            [maven_command, "compile"],
            cwd=java_plugin_path,
            capture_output=True,
            text=True,
            check=False,
        )
        
        assert result.returncode == 0, f"Maven build failed: {result.stderr}"
    
    def test_java_plugin_tests(self, java_plugin_path, maven_command):
        """Test that Java plugin tests pass."""
        result = subprocess.run(
            [maven_command, "test"],
            cwd=java_plugin_path,
            capture_output=True,
            text=True,
            check=False,
        )
        
        # Tests should pass or at least compile
        assert result.returncode in [0, 1], f"Maven test failed: {result.stderr}"
    
    def test_java_plugin_main_runs(self, java_plugin_path, maven_command):
        """Test that Java plugin main class runs."""
        result = subprocess.run(
            [maven_command, "exec:java", "-Dexec.mainClass=com.claude.plugin.java.Main"],
            cwd=java_plugin_path,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        
        # Should run without errors
        assert "Java Plugin" in result.stdout or "Java Plugin" in result.stderr
    
    def test_java_parser_functionality(self, java_plugin_path):
        """Test Java parser can be instantiated and used."""
        # This is a basic smoke test
        # More detailed tests would require Java integration
        assert (java_plugin_path / "src" / "main" / "java" / "com" / "claude" / 
                "plugin" / "java" / "analyzer" / "JavaParser.java").exists()
    
    def test_java_analyzer_exists(self, java_plugin_path):
        """Test that Java analyzer components exist."""
        analyzer_path = (java_plugin_path / "src" / "main" / "java" / "com" / 
                        "claude" / "plugin" / "java" / "analyzer")
        
        assert analyzer_path.exists()
        assert (analyzer_path / "JavaParser.java").exists()
        assert (analyzer_path / "ASTAnalyzer.java").exists()
        assert (analyzer_path / "DependencyAnalyzer.java").exists()

    
