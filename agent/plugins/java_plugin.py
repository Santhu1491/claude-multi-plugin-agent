"""Java plugin adapter."""

from .base_plugin import BasePlugin


class JavaPlugin(BasePlugin):
    def execute(self, request: dict) -> dict:
        return {"plugin": "java", "request": request}
