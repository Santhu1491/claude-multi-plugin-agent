"""Python plugin interface."""


class PythonPlugin:
    """Expose the Python plugin to the agent."""

    name = "python"

    def execute(self, request: dict) -> dict:
        """Execute a plugin request."""
        return {"plugin": self.name, "request": request}
