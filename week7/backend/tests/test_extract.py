from backend.app.services.extract import extract_action_items


def test_extract_action_items():
    text = """
    This is a note
    - TODO: write tests
    - ACTION: review PR
    - Ship it!
    Not actionable
    """.strip()
    items = extract_action_items(text)
    assert "TODO: write tests" in items
    assert "ACTION: review PR" in items
    assert "Ship it!" in items


def test_extract_checkboxes():
    text = """
    [ ] Uncompleted task
    [x] Completed task
    [X] Also completed
    Regular text
    """.strip()
    items = extract_action_items(text)
    assert "[ ] Uncompleted task" in items
    assert "[x] Completed task" in items
    assert "[X] Also completed" in items
    assert len(items) == 3


def test_extract_priority_markers():
    text = """
    HIGH: Critical bug fix
    P0: Security patch
    MEDIUM: Feature request
    LOW: Nice to have
    Regular text
    """.strip()
    items = extract_action_items(text)
    assert "HIGH: Critical bug fix" in items
    assert "P0: Security patch" in items
    assert "MEDIUM: Feature request" in items
    assert "LOW: Nice to have" in items


def test_extract_mentions():
    text = """
    Review this @john
    @alice can you test this
    No mention here
    Email: test@example.com should also match
    """.strip()
    items = extract_action_items(text)
    assert any("@john" in item for item in items)
    assert any("@alice" in item for item in items)
    assert any("@example" in item for item in items)


def test_extract_due_dates():
    text = """
    Complete by 2024-01-15
    Due 12/31/2023
    deadline 5pm tomorrow
    No date here
    """.strip()
    items = extract_action_items(text)
    assert any("by 2024" in item for item in items)
    assert any("Due 12" in item for item in items)
    assert any("deadline 5" in item for item in items)


def test_extract_numbered_lists():
    text = """
    1. First task
    2. TODO: Second task
    3. Third task with priority
    Regular text
    """.strip()
    items = extract_action_items(text)
    # Only the one with TODO should match since numbered items alone don't match other patterns
    assert "TODO: Second task" in items


