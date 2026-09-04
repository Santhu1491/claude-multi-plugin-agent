"""Self-healing execution result."""

from dataclasses import dataclass, field

from agent.models.quality_result import QualityResult


@dataclass
class HealingResult:
    """Represents the outcome of the self-healing workflow."""

    success: bool
    attempts: int
    quality_results: list[QualityResult] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    @property
    def exhausted(self) -> bool:
        return not self.success and self.attempts >= 3