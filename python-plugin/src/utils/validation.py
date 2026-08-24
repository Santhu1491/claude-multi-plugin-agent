"""Validation helpers for the Python plugin."""


def require_text(value: str, field_name: str = "value") -> str:
    """Return non-empty text or raise a validation error."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be non-empty text")
    return value
