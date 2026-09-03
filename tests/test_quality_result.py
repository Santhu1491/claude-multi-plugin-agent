from agent.models.quality_result import QualityResult


def test_quality_result_success():
    result = QualityResult(
        success=True,
        technology="python",
        checks_run=["pytest", "lint"],
        output="All checks passed",
    )

    assert result.success is True
    assert result.failed is False
    assert result.technology == "python"
    assert "pytest" in result.checks_run


def test_quality_result_failure():
    result = QualityResult(
        success=False,
        technology="java",
        checks_run=["maven"],
        errors="Compilation failed",
    )

    assert result.success is False
    assert result.failed is True
    assert result.errors == "Compilation failed"