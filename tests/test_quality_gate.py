from pathlib import Path

from agent.core.quality_gate import QualityGate


def test_quality_gate_python_success(tmp_path: Path):
    test_file = tmp_path / "test_sample.py"

    test_file.write_text(
        """
def test_sample():
    assert 1 + 1 == 2
""",
        encoding="utf-8",
    )

    gate = QualityGate(tmp_path)

    result = gate.run_python()

    print("\nQuality result:")
    print(result)

    assert result.success is True
    assert result.technology == "python"
    assert "pytest" in result.checks_run

def test_quality_gate_python_failure(tmp_path: Path):
    test_file = tmp_path / "test_sample.py"

    test_file.write_text(
        """
def test_sample():
    assert 1 + 1 == 3
""",
        encoding="utf-8",
    )

    gate = QualityGate(tmp_path)

    result = gate.run_python()

    assert result.success is False
    assert result.failed is True
    assert "pytest" in result.checks_run

def test_quality_gate_python_combined_success(tmp_path: Path):
    test_file = tmp_path / "test_sample.py"

    test_file.write_text(
        """
def test_sample():
    assert 1 + 1 == 2
""",
        encoding="utf-8",
    )

    gate = QualityGate(tmp_path)

    result = gate.run_python_checks()

    print("\nCombined Python quality result:")
    print(result)

    assert result.success is True
    assert "pytest" in result.checks_run
    assert "ruff" in result.checks_run

def test_quality_gate_java_success():
    java_plugin_path = (
        Path(__file__).resolve().parents[1]
        / "plugins"
        / "java-plugin"
    )

    gate = QualityGate(java_plugin_path)

    result = gate.run_java()

    print("\nJava quality result:")
    print(result)

    assert result.success is True
    assert result.technology == "java"
    assert "maven-test" in result.checks_run

def test_quality_gate_dispatches_python(tmp_path: Path):
    test_file = tmp_path / "test_sample.py"

    test_file.write_text(
        """
def test_sample():
    assert 1 + 1 == 2
""",
        encoding="utf-8",
    )

    gate = QualityGate(tmp_path)

    result = gate.run("python")

    assert result.success is True
    assert result.technology == "python"
    assert "pytest" in result.checks_run
    assert "ruff" in result.checks_run


def test_quality_gate_rejects_unknown_technology(tmp_path: Path):
    gate = QualityGate(tmp_path)

    result = gate.run("go")

    assert result.success is False
    assert result.failed is True
    assert "Unsupported technology" in result.errors