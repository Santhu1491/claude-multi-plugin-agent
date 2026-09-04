"""Self-healing retry workflow."""

from collections.abc import Callable

from agent.models.healing_result import HealingResult
from agent.models.quality_result import QualityResult


class SelfHealer:
    """Retries failed quality checks and applies repairs between attempts."""

    def __init__(self, max_attempts: int = 3) -> None:
        if max_attempts < 1:
            raise ValueError("max_attempts must be at least 1.")

        self.max_attempts = max_attempts

    def run(
        self,
        quality_check: Callable[[], QualityResult],
        repair: Callable[[QualityResult, int], None] | None = None,
    ) -> HealingResult:
        """Run checks and optionally repair failures before retrying."""

        quality_results: list[QualityResult] = []
        errors: list[str] = []

        for attempt in range(1, self.max_attempts + 1):
            result = quality_check()
            quality_results.append(result)

            if result.success:
                return HealingResult(
                    success=True,
                    attempts=attempt,
                    quality_results=quality_results,
                    errors=errors,
                )

            error_message = (
                result.errors
                or result.output
                or "Quality check failed."
            )
            errors.append(error_message)

            if attempt < self.max_attempts and repair is not None:
                repair(result, attempt)

        return HealingResult(
            success=False,
            attempts=self.max_attempts,
            quality_results=quality_results,
            errors=errors,
        )