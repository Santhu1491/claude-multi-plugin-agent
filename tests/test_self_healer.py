from agent.core.self_healer import SelfHealer
from agent.models.quality_result import QualityResult


def test_self_healer_succeeds_first_attempt():
    healer = SelfHealer()

    def quality_check():
        return QualityResult(
            success=True,
            technology="python",
            checks_run=["pytest"],
        )

    result = healer.run(quality_check)

    assert result.success is True
    assert result.attempts == 1
    assert len(result.quality_results) == 1


def test_self_healer_retries_until_success():
    healer = SelfHealer()

    attempts = {"count": 0}

    def quality_check():
        attempts["count"] += 1

        return QualityResult(
            success=attempts["count"] == 3,
            technology="python",
            checks_run=["pytest"],
            errors="" if attempts["count"] == 3 else "Tests failed",
        )

    result = healer.run(quality_check)

    assert result.success is True
    assert result.attempts == 3
    assert len(result.quality_results) == 3


def test_self_healer_stops_after_max_attempts():
    healer = SelfHealer(max_attempts=3)

    def quality_check():
        return QualityResult(
            success=False,
            technology="java",
            checks_run=["maven-test"],
            errors="Compilation failed",
        )

    result = healer.run(quality_check)

    assert result.success is False
    assert result.attempts == 3
    assert result.exhausted is True
    assert len(result.quality_results) == 3

def test_self_healer_calls_repair_after_failure():
    healer = SelfHealer()

    attempts = {"count": 0}
    repairs = []

    def quality_check():
        attempts["count"] += 1

        return QualityResult(
            success=attempts["count"] == 2,
            technology="python",
            checks_run=["pytest"],
            errors="" if attempts["count"] == 2 else "Tests failed",
        )

    def repair(result, attempt):
        repairs.append((result.errors, attempt))

    result = healer.run(
        quality_check=quality_check,
        repair=repair,
    )

    assert result.success is True
    assert result.attempts == 2
    assert repairs == [("Tests failed", 1)]


def test_self_healer_does_not_repair_after_final_attempt():
    healer = SelfHealer(max_attempts=3)

    repairs = []

    def quality_check():
        return QualityResult(
            success=False,
            technology="java",
            checks_run=["maven-test"],
            errors="Compilation failed",
        )

    def repair(result, attempt):
        repairs.append(attempt)

    result = healer.run(
        quality_check=quality_check,
        repair=repair,
    )

    assert result.success is False
    assert repairs == [1, 2]