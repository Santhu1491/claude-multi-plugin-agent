"""Subprocess-based Python execution sandbox."""

import subprocess
import sys
import tempfile
from pathlib import Path


class Sandbox:
    """Runs Python code in a separate subprocess."""

    def execute(
        self,
        code: str,
        timeout: int = 10,
    ) -> dict:
        """Execute code with timeout isolation."""

        with tempfile.TemporaryDirectory() as temp_dir:
            script_path = Path(temp_dir) / "sandbox.py"

            script_path.write_text(
                code,
                encoding="utf-8",
            )

            try:
                result = subprocess.run(
                    [
                        sys.executable,
                        "-I",
                        str(script_path),
                    ],
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                    check=False,
                    cwd=temp_dir,
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
                        f"Sandbox execution timed out "
                        f"after {timeout} seconds"
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