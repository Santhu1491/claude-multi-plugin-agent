from agent.core.git_workflow import GitWorkflow


class FakeGitClient:
    def __init__(self):
        self.calls = []

    def create_branch(self, branch_name):
        self.calls.append(
            ("create_branch", branch_name)
        )
        return branch_name

    def stage_all(self):
        self.calls.append(
            ("stage_all",)
        )

    def commit(self, message):
        self.calls.append(
            ("commit", message)
        )
        return "abc123"

    def push(self, branch_name):
        self.calls.append(
            ("push", branch_name)
        )


class FakeGitHubClient:
    def __init__(self):
        self.calls = []

    def create_pull_request(
        self,
        title,
        head,
        base,
        body,
    ):
        self.calls.append(
            (
                "create_pull_request",
                title,
                head,
                base,
                body,
            )
        )

        return {
            "number": 42,
            "html_url": "https://github.com/test/repo/pull/42",
        }


def test_git_workflow_publish_changes():
    git_client = FakeGitClient()
    github_client = FakeGitHubClient()

    workflow = GitWorkflow(
        git_client=git_client,
        github_client=github_client,
    )

    result = workflow.publish_changes(
        branch_name="feature/test",
        commit_message="feat: test",
        pr_title="Test PR",
        pr_body="Test body",
    )

    assert result["branch"] == "feature/test"
    assert result["commit"] == "abc123"
    assert result["pr_number"] == 42
    assert "pull/42" in result["pr_url"]

    assert git_client.calls == [
        ("create_branch", "feature/test"),
        ("stage_all",),
        ("commit", "feat: test"),
        ("push", "feature/test"),
    ]