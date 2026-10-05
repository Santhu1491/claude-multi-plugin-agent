"""Deterministic fake LLM client for tests."""


class FakeLLM:
    """Fake language model with predictable responses."""

    def __init__(self) -> None:
        self.prompts: list[str] = []

    def generate(self, prompt: str) -> str:
        """Return a deterministic response based on prompt type."""

        self.prompts.append(prompt)

        if "selecting relevant repository files" in prompt:
            return "agent/utils/__init__.py"

        if "Return ONLY valid JSON" in prompt:
            return """
[
  {
    "path": "agent/utils/live_validation.py",
    "action": "create",
    "reason": "Add requested validation function"
  }
]
""".strip()

        if "Generate the COMPLETE final content for this file" in prompt:
            return (
                'def hello_validation() -> str:\n'
                '    return "hello from live validation"\n'
            )

        if "repairing a software repository change" in prompt:
            return (
                'def hello_validation() -> str:\n'
                '    return "hello from live validation"\n'
            )

        return """
Technology: python

Understanding:
Add a simple validation function.

Relevant Files:
agent/utils/__init__.py

Plan:
1. Create the validation module.
2. Add the requested function.
3. Run quality checks.
""".strip()