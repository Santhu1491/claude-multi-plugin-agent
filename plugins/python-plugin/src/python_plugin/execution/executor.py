"""Python code execution utilities."""

import subprocess
import sys
import tempfile
from pathlib import Path


class Executor:
    """Executes Python code in a separate subprocess."""

    def execute(
        self,
        code: str,
        timeout: int = 30,
    ) -> dict:
        """Execute Python code and capture output."""

        with tempfile.TemporaryDirectory() as temp_dir:
            script_path = Path(temp_dir) / "script.py"

            script_path.write_text(
                code,
                encoding="utf-8",
            )

            try:
                result = subprocess.run(
                    [
                        sys.executable,
                        str(script_path),
                    ],
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                    check=False,
                )

                return {
                    "success": result.returncode == 0,
                    "output": result.stdout,
                    "error": result.stderr,
                    "return_code": result.returncode,
                }

            except subprocess.TimeoutExpired:
                return {
                    "success": False,
                    "output": "",
                    "error": (
                        f"Execution timed out after "
                        f"{timeout} seconds"
                    ),
                    "return_code": None,
                }

            except OSError as exc:
                return {
                    "success": False,
                    "output": "",
                    "error": str(exc),
                    "return_code": None,
                }

    def execute_function(
        self,
        code: str,
        function_name: str,
        timeout: int = 30,
    ) -> dict:
        """Execute a named function from generated Python code."""

        wrapper_code = (
            f"{code}\n\n"
            f"if '{function_name}' not in globals():\n"
            f"    raise RuntimeError("
            f"'Function {function_name} not found')\n"
            f"\n"
            f"result = globals()['{function_name}']()\n"
            f"print(repr(result))\n"
        )

        return self.execute(
            wrapper_code,
            timeout=timeout,
        )