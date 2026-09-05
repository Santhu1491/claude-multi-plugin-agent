"""Application configuration."""

import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Central application settings loaded from environment variables."""

    def __init__(self) -> None:
        self.anthropic_api_key = os.getenv(
            "ANTHROPIC_API_KEY"
        )

        self.log_level = os.getenv(
            "LOG_LEVEL",
            "INFO",
        )

        self.max_retries = int(
            os.getenv(
                "MAX_RETRIES",
                "3",
            )
        )

        self.timeout = int(
            os.getenv(
                "TIMEOUT",
                "30",
            )
        )

        self.plugin_directory = os.getenv(
            "PLUGIN_DIRECTORY",
            "plugins",
        )

        self.version = os.getenv(
            "APP_VERSION",
            "0.1.0",
        )

        self.azure_devops_org = os.getenv(
            "AZURE_DEVOPS_ORG"
        )

        self.azure_devops_project = os.getenv(
            "AZURE_DEVOPS_PROJECT"
        )

        self.azure_devops_pat = os.getenv(
            "AZURE_DEVOPS_PAT"
        )

        self.azure_devops_repository = os.getenv(
            "AZURE_DEVOPS_REPOSITORY"
        )

        self.default_branch = os.getenv(
            "DEFAULT_BRANCH",
            "main",
        )

        self.self_heal_max_attempts = int(
            os.getenv(
                "SELF_HEAL_MAX_ATTEMPTS",
                "3",
            )
        )

        self.maven_home = os.getenv(
            "MAVEN_HOME"
        )