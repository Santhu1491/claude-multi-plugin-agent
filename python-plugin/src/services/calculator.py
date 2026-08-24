"""Calculator service."""


def calculate(left: float, right: float, operation: str) -> float:
    """Apply a basic arithmetic operation."""
    operations = {
        "add": lambda: left + right,
        "subtract": lambda: left - right,
        "multiply": lambda: left * right,
        "divide": lambda: left / right,
    }
    if operation not in operations:
        raise ValueError(f"Unsupported operation: {operation}")
    if operation == "divide" and right == 0:
        raise ValueError("Cannot divide by zero")
    return operations[operation]()
