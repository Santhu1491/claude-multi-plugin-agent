from agent.core.repair_generator import RepairGenerator
from agent.models.proposed_change import ProposedChange
from agent.models.quality_result import QualityResult


class FakeClaude:
    def generate(self, prompt: str) -> str:
        assert "Tests failed" in prompt
        assert "sample.py" in prompt

        return "def add(a, b):\n    return a + b\n"


def test_repair_generator_returns_updated_change():
    generator = RepairGenerator(FakeClaude())

    change = ProposedChange(
        path="sample.py",
        action="modify",
        reason="Fix add function",
        original_content="def add(a, b):\n    return a + b\n",
        generated_content="def add(a, b):\n    return a - b\n",
    )

    quality_result = QualityResult(
        success=False,
        technology="python",
        checks_run=["pytest"],
        errors="Tests failed",
    )

    repaired = generator.repair_change(
        request={"content": "Fix add function"},
        change=change,
        quality_result=quality_result,
        repository_context="sample.py",
    )

    assert repaired.path == "sample.py"
    assert repaired.original_content == change.original_content
    assert "return a + b" in repaired.generated_content