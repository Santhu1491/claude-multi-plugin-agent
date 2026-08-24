"""Sample data processing module."""

from typing import Any


class DataProcessor:
    """Process and transform data."""
    
    def filter_records(self, records: list[dict[str, Any]], key: str, value: Any) -> list[dict[str, Any]]:
        """Filter records by key-value pair."""
        return [record for record in records if record.get(key) == value]
    
    def sort_records(self, records: list[dict[str, Any]], key: str, reverse: bool = False) -> list[dict[str, Any]]:
        """Sort records by a specific key."""
        return sorted(records, key=lambda x: x.get(key, ""), reverse=reverse)
    
    def group_by(self, records: list[dict[str, Any]], key: str) -> dict[Any, list[dict[str, Any]]]:
        """Group records by a specific key."""
        groups: dict[Any, list[dict[str, Any]]] = {}
        
        for record in records:
            group_key = record.get(key)
            if group_key not in groups:
                groups[group_key] = []
            groups[group_key].append(record)
        
        return groups
    
    def transform(self, records: list[dict[str, Any]], transformer: callable) -> list[dict[str, Any]]:
        """Apply a transformation function to all records."""
        return [transformer(record) for record in records]


def main() -> None:
    """Demonstrate data processor usage."""
    processor = DataProcessor()
    
    # Sample data
    records = [
        {"id": 1, "name": "Alice", "age": 30, "city": "New York"},
        {"id": 2, "name": "Bob", "age": 25, "city": "London"},
        {"id": 3, "name": "Charlie", "age": 35, "city": "New York"},
        {"id": 4, "name": "Diana", "age": 28, "city": "Paris"},
    ]
    
    print("Data Processor Demo")
    
    # Filter
    ny_residents = processor.filter_records(records, "city", "New York")
    print(f"\nNew York residents: {len(ny_residents)}")
    
    # Sort
    sorted_by_age = processor.sort_records(records, "age")
    print(f"\nSorted by age: {[r['name'] for r in sorted_by_age]}")
    
    # Group
    by_city = processor.group_by(records, "city")
    print(f"\nGrouped by city: {list(by_city.keys())}")


if __name__ == "__main__":
    main()
