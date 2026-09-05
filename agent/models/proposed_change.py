import difflib
from dataclasses import dataclass


@dataclass
class ProposedChange:
    """Represents a generated repository change before it is applied."""

    path: str
    action: str
    reason: str
    original_content: str | None
    generated_content: str

    def build_diff(self) -> str:
        """Return a unified diff for this proposed change."""

        original = (
            self.original_content.splitlines(keepends=True)
            if self.original_content is not None
            else []
        )

        generated = self.generated_content.splitlines(
            keepends=True
        )

        diff = difflib.unified_diff(
            original,
            generated,
            fromfile=f"a/{self.path}",
            tofile=f"b/{self.path}",
        )

        return "".join(diff)