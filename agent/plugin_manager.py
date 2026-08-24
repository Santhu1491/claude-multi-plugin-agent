"""Plugin registration and lookup."""


class PluginManager:
    def __init__(self) -> None:
        self._plugins: dict[str, object] = {}

    def register(self, name: str, plugin: object) -> None:
        self._plugins[name] = plugin

    def get(self, name: str) -> object:
        return self._plugins[name]
