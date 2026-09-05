from agent.config.settings import Settings


def test_settings_load_defaults(monkeypatch):
    monkeypatch.delenv(
        "DEFAULT_BRANCH",
        raising=False,
    )

    monkeypatch.delenv(
        "SELF_HEAL_MAX_ATTEMPTS",
        raising=False,
    )

    settings = Settings()

    assert settings.default_branch == "main"
    assert settings.self_heal_max_attempts == 3


def test_settings_load_environment(monkeypatch):
    monkeypatch.setenv(
        "AZURE_DEVOPS_ORG",
        "test-org",
    )

    monkeypatch.setenv(
        "AZURE_DEVOPS_PROJECT",
        "test-project",
    )

    monkeypatch.setenv(
        "AZURE_DEVOPS_REPOSITORY",
        "test-repo",
    )

    monkeypatch.setenv(
        "DEFAULT_BRANCH",
        "develop",
    )

    monkeypatch.setenv(
        "SELF_HEAL_MAX_ATTEMPTS",
        "5",
    )

    settings = Settings()

    assert settings.azure_devops_org == "test-org"
    assert settings.azure_devops_project == "test-project"
    assert settings.azure_devops_repository == "test-repo"
    assert settings.default_branch == "develop"
    assert settings.self_heal_max_attempts == 5