"""File analysis service."""

from pathlib import Path


def analyze_file(path: str | Path) -> dict[str, int | str]:
    """Return basic metadata for a text file."""
    file_path = Path(path)
    text = file_path.read_text(encoding="utf-8")
    return {
        "path": str(file_path),
        "characters": len(text),
        "lines": len(text.splitlines()),
    }
