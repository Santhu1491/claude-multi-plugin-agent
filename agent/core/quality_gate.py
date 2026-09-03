"""Repository quality gate."""

import subprocess
from pathlib import Path

from agent.models.quality_result import QualityResult


class QualityGate:
    """Runs technology-specific repository quality checks."""

    def __init__(self, root_path: str | Path) -> None:
        self.root = Path(root_path).resolve()

        if not self.root.exists():
            raise ValueError(f"Repository does not exist: {self.root}")

    def run_python(self) -> QualityResult:
        """Run Python quality checks."""

        command = [
            "pytest",
            "-q",
        ]

        result = subprocess.run(
            command,
            cwd=self.root,
            capture_output=True,
            text=True,
        )

        success = result.returncode == 0

        return QualityResult(
            success=success,
            technology="python",
            checks_run=["pytest"],
            output=result.stdout.strip(),
            errors=result.stderr.strip(),
        )

    def run_python_lint(self) -> QualityResult:
        """Run Python lint checks using Ruff."""

        command = [
            "ruff",
            "check",
            ".",
        ]

        try:
            result = subprocess.run(
                command,
                cwd=self.root,
                capture_output=True,
                text=True,
            )
        except FileNotFoundError:
            return QualityResult(
                success=False,
                technology="python",
                checks_run=["ruff"],
                errors="Ruff is not installed or not available in PATH.",
            )

        return QualityResult(
            success=result.returncode == 0,
            technology="python",
            checks_run=["ruff"],
            output=result.stdout.strip(),
            errors=result.stderr.strip(),
        )

    def run_python_checks(self) -> QualityResult:
        """Run all Python quality checks."""

        test_result = self.run_python()

        if not test_result.success:
            return QualityResult(
                success=False,
                technology="python",
                checks_run=test_result.checks_run,
                output=test_result.output,
                errors=test_result.errors,
            )

        lint_result = self.run_python_lint()

        return QualityResult(
            success=lint_result.success,
            technology="python",
            checks_run=[
                *test_result.checks_run,
                *lint_result.checks_run,
            ],
            output="\n".join(
                part
                for part in [
                    test_result.output,
                    lint_result.output,
                ]
                if part
            ),
            errors="\n".join(
                part
                for part in [
                    test_result.errors,
                    lint_result.errors,
                ]
                if part
            ),
        )

    def run_java(self) -> QualityResult:
        """Run Java quality checks using Maven."""

        maven_command = [
            r"C:\Program Files\Apache\maven\apache-maven-3.9.16\bin\mvn.cmd",
            "test",
        ]

        try:
            result = subprocess.run(
                maven_command,
                cwd=self.root,
                capture_output=True,
                text=True,
                timeout=120,
            )
        except FileNotFoundError:
            return QualityResult(
                success=False,
                technology="java",
                checks_run=["maven-test"],
                errors="Maven could not be found.",
            )
        except subprocess.TimeoutExpired:
            return QualityResult(
                success=False,
                technology="java",
                checks_run=["maven-test"],
                errors="Maven quality check timed out.",
            )

        return QualityResult(
            success=result.returncode == 0,
            technology="java",
            checks_run=["maven-test"],
            output=result.stdout.strip(),
            errors=result.stderr.strip(),
        )

    def run(self, technology: str) -> QualityResult:
        """Run quality checks for the requested technology."""
    
        normalized = technology.strip().lower()
    
        if normalized == "python":
            return self.run_python_checks()
    
        if normalized == "java":
            return self.run_java()
    
        return QualityResult(
            success=False,
            technology=normalized,
            checks_run=[],
            errors=f"Unsupported technology: {technology}",
        )