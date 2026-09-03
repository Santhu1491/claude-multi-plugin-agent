from agent.core.code_generator import CodeGenerator
from agent.core.workspace import Workspace
from agent.models.proposed_change import ProposedChange


class ChangeBuilder:
    """Builds proposed repository changes without writing them."""

    def __init__(
        self,
        workspace: Workspace,
        generator: CodeGenerator,
    ) -> None:
        self.workspace = workspace
        self.generator = generator

    def build_changes(
        self,
        request: dict,
        change_plan: list[dict[str, str]],
        repository_context: str,
    ) -> list[ProposedChange]:

        proposed_changes: list[ProposedChange] = []

        for change in change_plan:
            path = change["path"]
            action = change["action"]

            original_content = None

            if action == "modify":
                original_content = self.workspace.read_file(path)

            generated_content = (
                self.generator.generate_file_content(
                    request=request,
                    change=change,
                    existing_content=original_content,
                    repository_context=repository_context,
                )
            )

            proposed_changes.append(
                ProposedChange(
                    path=path,
                    action=action,
                    reason=change["reason"],
                    original_content=original_content,
                    generated_content=generated_content,
                )
            )

        return proposed_changes