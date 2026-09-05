"""Resolve external development tools."""

import os
import shutil
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(override=True)

class ToolResolver:
    """Find executable paths for required development tools."""

    @staticmethod
    def find(command: str) -> str | None:
        """Find a command using PATH."""

        return shutil.which(command)

    @staticmethod
    def find_maven() -> str | None:
        """Find Maven using PATH or MAVEN_HOME."""
    
        command = shutil.which("mvn")
    
        if command:
            return command
    
        maven_home = os.getenv("MAVEN_HOME")
    
        if not maven_home:
            return None
    
        maven_home = maven_home.strip().strip('"').strip("'")
    
        candidates = [
            Path(maven_home) / "bin" / "mvn.cmd",
            Path(maven_home) / "bin" / "mvn",
        ]
    
        for candidate in candidates:
            if candidate.exists():
                return str(candidate)
    
        return None