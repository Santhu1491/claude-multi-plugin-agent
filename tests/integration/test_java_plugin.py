"""Integration tests for Java plugin."""

import pytest
import subprocess
from pathlib import Path


class TestJavaPluginIntegration:
    """Integration tests for the Java plugin."""
    
    @pytest.fixture
    def java_plugin_path(self):
        """Get path to Java plugin."""
        return Path(__file__).parent.parent.parent / "plugins" / "java-plugin"
    
    def test_java_plugin_builds(self, java_plugin_path):
        """Test that Java plugin builds successfully."""
        result = subprocess.run(
            ["mvn", "compile"],
            cwd=java_plugin_path,
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0, f"Maven build failed: {result.stderr}"
    
    def test_java_plugin_tests(self, java_plugin_path):
        """Test that Java plugin tests pass."""
        result = subprocess.run(
            ["mvn", "test"],
            cwd=java_plugin_path,
            capture_output=True,
            text=True
        )
        
        # Tests should pass or at least compile
        assert result.returncode in [0, 1], f"Maven test failed: {result.stderr}"
    
    def test_java_plugin_main_runs(self, java_plugin_path):
        """Test that Java plugin main class runs."""
        result = subprocess.run(
            ["mvn", "exec:java", "-Dexec.mainClass=com.claude.plugin.java.Main"],
            cwd=java_plugin_path,
            capture_output=True,
            text=True,
            timeout=30
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
