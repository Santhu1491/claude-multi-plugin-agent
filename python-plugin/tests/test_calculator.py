from src.services.calculator import calculate


def test_calculate_addition() -> None:
    assert calculate(2, 3, "add") == 5
