"""Sample Python application for testing the plugin."""


def main() -> None:
    """Main entry point."""
    print("Sample Python Application")
    
    # Demonstrate basic functionality
    result = calculate(10, 20)
    print(f"Calculation result: {result}")
    
    # Process some data
    data = {"name": "John", "age": 30, "city": "New York"}
    process_data(data)


def calculate(a: int, b: int) -> int:
    """Perform a simple calculation."""
    return a + b


def process_data(data: dict) -> None:
    """Process dictionary data."""
    print("Processing data:")
    for key, value in data.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
