"""Claude client integration boundary."""


class ClaudeClient:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
