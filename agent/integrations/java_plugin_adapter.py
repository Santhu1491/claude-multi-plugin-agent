"""Adapter for communicating with the Java plugin."""

import subprocess
import os
import shutil
from pathlib import Path
from typing import Any


class JavaPluginAdapter:
    """Allows the Python agent to execute the Java plugin."""

    name = "java"

    def __init__(self) -> None:
        project_root = Path(__file__).resolve().parents[2]

        self.java_plugin_path = (
            project_root
            / "plugins"
            / "java-plugin"
        )

    def execute(
        self,
        request: dict[str, Any],
    ) -> dict[str, Any]:

        operation = request.get("operation", "execute")
        parameters = request.get("parameters", {})

        payload = str(parameters)

        maven_command = shutil.which("mvn")

        if not maven_command:
            maven_home = os.getenv("MAVEN_HOME")

            if maven_home:
                candidate = Path(maven_home) / "bin" / "mvn.cmd"

                if candidate.exists():
                    maven_command = str(candidate)

        if not maven_command:
            fallback = Path(
                r"C:\Program Files\Apache\maven\apache-maven-3.9.16\bin\mvn.cmd"
            )
        
            if fallback.exists():
                maven_command = str(fallback)
        
        if not maven_command:
            return {
                "success": False,
                "error": "Maven could not be found. Check MAVEN_HOME or PATH.",
            }

        try:
            command = [
                maven_command,
                "-q",
                "-f",
                str(self.java_plugin_path / "pom.xml"),
                "org.codehaus.mojo:exec-maven-plugin:3.1.0:java",
                "-Dexec.mainClass=com.claude.plugin.java.Main",
                f"-Dexec.args={operation} \"{payload}\"",
            ]

            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=60,
            )

            output = result.stdout.strip()

            if result.returncode != 0:
                return {
                    "success": False,
                    "error": result.stderr.strip(),
                }

            if "SUCCESS|" in output:
                message = output.split("SUCCESS|", 1)[1]

                return {
                    "success": True,
                    "data": message,
                }

            return {
                "success": False,
                "error": output or "Java plugin returned no output",
            }

        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Java plugin execution timed out",
            }

        except Exception as exc:
            return {
                "success": False,
                "error": str(exc),
            }