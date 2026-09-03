from agent.models.proposed_change import ProposedChange


def test_proposed_change_builds_diff():
    change = ProposedChange(
        path="app.py",
        action="modify",
        reason="Update message",
        original_content="print('old')\n",
        generated_content="print('new')\n",
    )

    diff = change.build_diff()

    print("\nGenerated diff:")
    print(diff)

    assert "--- a/app.py" in diff
    assert "+++ b/app.py" in diff
    assert "-print('old')" in diff
    assert "+print('new')" in diff


def test_proposed_change_diff_for_new_file():
    change = ProposedChange(
        path="new.py",
        action="create",
        reason="Create module",
        original_content=None,
        generated_content="print('new')\n",
    )

    diff = change.build_diff()

    assert "+print('new')" in diff