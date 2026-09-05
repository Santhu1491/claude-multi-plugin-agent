"""Request routing logic."""



class Router:
    """Routes requests to appropriate plugins based on content analysis."""

    def __init__(self):
        self.routes = {
            "python": ["python", "pytest", "pip"],
            "java": ["java", "compile", "maven", "spring"],
        }

    def route(self, request: dict) -> str:
        """Determine which plugin should handle the request."""

        technology = request.get("technology")

        if technology:
            normalized = str(technology).strip().lower()

            if normalized in self.routes:
                return normalized

        content = request.get("content", "").lower()

        for plugin_name, keywords in self.routes.items():
            if any(
                keyword in content
                for keyword in keywords
            ):
                return plugin_name

        return "python"

    def register_route(self, plugin_name: str, keywords: list[str]) -> None:
        """Register routing keywords for a plugin."""
        self.routes[plugin_name] = keywords
