from src.services.text_analyzer import analyze_text


def test_analyze_text() -> None:
    assert analyze_text("hello world hello")["words"] == 3
