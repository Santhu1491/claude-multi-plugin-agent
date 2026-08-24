"""Test execution functionality."""

import subprocess
from typing import Any


class TestRunner:
    """Run Python tests using pytest."""

    def run(self, path: str = "tests", verbose: bool = False) -> dict[str, Any]:
        """Run tests in the specified path."""
        cmd = ["pytest", path]
        
        if verbose:
            cmd.append("-v")
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            return {
                "success": result.returncode == 0,
                "exit_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Tests timed out after 60 seconds"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def run_file(self, file_path: str) -> dict[str, Any]:
        """Run tests in a specific file."""
        return self.run(file_path, verbose=True)

    def run_function(self, file_path: str, function_name: str) -> dict[str, Any]:
        """Run a specific test function."""
        test_spec = f"{file_path}::{function_name}"
        return self.run(test_spec, verbose=True)
