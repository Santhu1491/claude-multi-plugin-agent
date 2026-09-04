from pathlib import Path

from agent.core.healing_executor import HealingExecutor
from agent.core.workspace_writer import WorkspaceWriter
from agent.models.proposed_change import ProposedChange
from agent.models.quality_result import QualityResult


class FakeRepairGenerator:
    def repair_change(
        self,
        request,
        change,
        quality_result,
        repository_context,
    ):
        return ProposedChange(
            path=change.path,
            action=change.action,
            reason=change.reason,
            original_content=change.original_content,
            generated_content="fixed content",
        )


def test_healing_executor_repairs_failed_change(tmp_path: Path):
    writer = WorkspaceWriter(tmp_path)

    file_path = tmp_path / "sample.py"
    file_path.write_text(
        "original content",
        encoding="utf-8",
    )

    change = ProposedChange(
        path="sample.py",
        action="modify",
        reason="Update sample",
        original_content="original content",
        generated_content="broken content",
    )

    checks = {"count": 0}

    def quality_check():
        checks["count"] += 1

        success = checks["count"] == 2

        return QualityResult(
            success=success,
            technology="python",
            checks_run=["pytest"],
            errors="" if success else "Tests failed",
        )

    executor = HealingExecutor(
        writer=writer,
        repair_generator=FakeRepairGenerator(),
        quality_gate=FakeQualityGate(),
    )

    result = executor.execute(
        request={"content": "Update sample"},
        change=change,
        repository_context="sample.py",
        technology="python",
    )

    assert result.success is True
    assert result.attempts == 2
    assert file_path.read_text(
        encoding="utf-8"
    ) == "fixed content"

def test_healing_executor_rolls_back_after_failure(tmp_path: Path):
    writer = WorkspaceWriter(tmp_path)

    file_path = tmp_path / "sample.py"
    file_path.write_text(
        "original content",
        encoding="utf-8",
    )

    change = ProposedChange(
        path="sample.py",
        action="modify",
        reason="Update sample",
        original_content="original content",
        generated_content="broken content",
    )

    def quality_check():
        return QualityResult(
            success=False,
            technology="python",
            checks_run=["pytest"],
            errors="Tests still failing",
        )

    executor = HealingExecutor(
        writer=writer,
        repair_generator=FakeRepairGenerator(),
        quality_gate=AlwaysFailQualityGate(),
        max_attempts=3,
    )

    result = executor.execute(
        request={"content": "Update sample"},
        change=change,
        repository_context="sample.py",
        technology="python",
    )

    assert result.success is False
    assert result.attempts == 3

    assert file_path.read_text(
        encoding="utf-8"
    ) == "original content"

class FakeQualityGate:
    def __init__(self):
        self.calls = 0

    def run(self, technology):
        self.calls += 1

        success = self.calls == 2

        return QualityResult(
            success=success,
            technology=technology,
            checks_run=["pytest"],
            errors="" if success else "Tests failed",
        )

class AlwaysFailQualityGate:
    def run(self, technology):
        return QualityResult(
            success=False,
            technology=technology,
            checks_run=["pytest"],
            errors="Tests still failing",
        )