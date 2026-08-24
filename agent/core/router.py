"""Request routing logic."""

from typing import Any


class Router:
    """Routes requests to appropriate plugins based on content analysis."""

    def __init__(self) -> None:
        self.routes: dict[str, list[str]] = {
            "python": ["analyze", "parse", "python", "code"],
            "java": ["compile", "maven", "java", "spring"],
        }

    def route(self, request: dict[str, Any]) -> str:
        """Determine which plugin should handle the request."""
        content = str(request.get("content", "")).lower()
        
        for plugin, keywords in self.routes.items():
            if any(keyword in content for keyword in keywords):
                return plugin
        
        # Default to Python plugin
        return "python"

    def register_route(self, plugin_name: str, keywords: list[str]) -> None:
        """Register routing keywords for a plugin."""
        self.routes[plugin_name] = keywords
