"""Quality gate result model."""

from dataclasses import dataclass, field


@dataclass
class QualityResult:
    """Represents the result of repository quality checks."""

    success: bool
    technology: str
    checks_run: list[str] = field(default_factory=list)
    output: str = ""
    errors: str = ""

    @property
    def failed(self) -> bool:
        return not self.success