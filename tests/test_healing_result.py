from agent.models.healing_result import HealingResult


def test_healing_result_success():
    result = HealingResult(
        success=True,
        attempts=1,
    )

    assert result.success is True
    assert result.attempts == 1
    assert result.exhausted is False


def test_healing_result_exhausted():
    result = HealingResult(
        success=False,
        attempts=3,
        errors=["Tests failed"],
    )

    assert result.success is False
    assert result.exhausted is True
    assert "Tests failed" in result.errors