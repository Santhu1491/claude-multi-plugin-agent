import os

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()


class ClaudeClient:
    """Client responsible for communicating with Claude."""

    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")

        if not api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY is not configured."
            )

        self.client = Anthropic(api_key=api_key)

    def generate(self, prompt: str) -> str:
        """Send a prompt to Claude and return the response."""

        response = self.client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=2048,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response.content[0].text