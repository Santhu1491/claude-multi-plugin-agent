"""Select repository files relevant to a development request."""

from agent.integrations.claude import ClaudeClient


class FileSelector:
    """Uses Claude to identify relevant files from a repository tree."""

    def __init__(self, claude: ClaudeClient) -> None:
        self.claude = claude

    def select_files(
        self,
        request: dict,
        file_tree: str,
    ) -> list[str]:

        prompt = f"""
You are selecting relevant repository files for a software development task.

Development request:
{request}

Repository files:
{file_tree}

Return only repository-relative file paths that are relevant to the task.

Rules:
- Prefer existing files.
- Do not invent paths.
- Return one file path per line.
- Do not include explanations.
- Do not use bullets or numbering.
- Return at most 10 files.
"""

        response = self.claude.generate(prompt)

        selected_files = []

        for line in response.splitlines():
            path = line.strip()

            if not path:
                continue

            if path.startswith("- "):
                path = path[2:].strip()

            selected_files.append(path)

        return selected_files[:10]