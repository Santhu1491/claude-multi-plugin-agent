from pathlib import Path

from agent.utils.tool_resolver import ToolResolver


def test_tool_resolver_find(monkeypatch):
    monkeypatch.setattr(
        "agent.utils.tool_resolver.shutil.which",
        lambda command: "/usr/bin/git"
        if command == "git"
        else None,
    )

    assert ToolResolver.find("git") == "/usr/bin/git"
    assert ToolResolver.find("missing") is None


def test_find_maven_from_path(monkeypatch):
    monkeypatch.setattr(
        "agent.utils.tool_resolver.shutil.which",
        lambda command: "C:/tools/mvn.cmd"
        if command == "mvn"
        else None,
    )

    result = ToolResolver.find_maven()

    assert result == "C:/tools/mvn.cmd"


def test_find_maven_from_maven_home(
    tmp_path: Path,
    monkeypatch,
):
    maven_home = tmp_path / "maven"
    bin_dir = maven_home / "bin"
    bin_dir.mkdir(parents=True)

    mvn_cmd = bin_dir / "mvn.cmd"
    mvn_cmd.write_text("", encoding="utf-8")

    monkeypatch.setattr(
        "agent.utils.tool_resolver.shutil.which",
        lambda command: None,
    )

    monkeypatch.setenv(
        "MAVEN_HOME",
        str(maven_home),
    )

    result = ToolResolver.find_maven()

    assert result == str(mvn_cmd)


def test_find_maven_missing(monkeypatch):
    monkeypatch.setattr(
        "agent.utils.tool_resolver.shutil.which",
        lambda command: None,
    )

    monkeypatch.delenv(
        "MAVEN_HOME",
        raising=False,
    )

    assert ToolResolver.find_maven() is None