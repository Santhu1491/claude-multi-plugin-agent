"""Sample Python code for testing."""


def calculate_sum(numbers: list[int]) -> int:
    """Calculate the sum of a list of numbers."""
    return sum(numbers)


def calculate_average(numbers: list[int]) -> float:
    """Calculate the average of a list of numbers."""
    if not numbers:
        return 0.0
    return sum(numbers) / len(numbers)


class DataAnalyzer:
    """Analyze data."""
    
    def __init__(self, data: list) -> None:
        """Initialize with data."""
        self.data = data
    
    def count(self) -> int:
        """Count items."""
        return len(self.data)
    
    def find_max(self) -> int:
        """Find maximum value."""
        return max(self.data) if self.data else 0
    
    def find_min(self) -> int:
        """Find minimum value."""
        return min(self.data) if self.data else 0
