"""Text analysis service."""

from collections import Counter


def analyze_text(text: str) -> dict[str, int | str]:
    """Return basic text statistics."""
    words = text.split()
    return {
        "characters": len(text),
        "words": len(words),
        "most_common_word": Counter(words).most_common(1)[0][0] if words else "",
    }
