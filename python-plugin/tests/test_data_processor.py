from src.services.data_processor import process_records


def test_process_records_materializes_input() -> None:
    assert process_records(iter([{"id": 1}])) == [{"id": 1}]
