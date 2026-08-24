"""Python plugin adapter."""

from .base_plugin import BasePlugin


class PythonPlugin(BasePlugin):
    def execute(self, request: dict) -> dict:
        return {"plugin": "python", "request": request}
