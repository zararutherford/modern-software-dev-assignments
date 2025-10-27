from backend.app.services.extract import extract_action_items, extract_hashtags


def test_extract_action_items():
    text = """
    This is a note
    - TODO: write tests
    - Ship it!
    - [ ] checkbox task
    Not actionable
    """.strip()
    items = extract_action_items(text)
    assert "write tests" in items or "TODO: write tests" in items
    assert "Ship it!" in items
    assert "checkbox task" in items


def test_extract_hashtags():
    text = "Random #Tag1 and #tag2 and #tag1 again"
    tags = extract_hashtags(text)
    assert set(tags) == {"tag1", "tag2"}


def test_extract_endpoint_apply(client):
    # Create a note with hashtags and checkbox
    payload = {"title": "X", "content": "Do this\n- [ ] task1\n#alpha #beta"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201
    note_id = r.json()["id"]

    r = client.post(f"/notes/{note_id}/extract", params={"apply": True})
    assert r.status_code == 200
    data = r.json()
    assert set(data.keys()) == {"tags", "action_items", "applied"}
    assert data["applied"] is True
    assert "task1" in data["action_items"]

    # Action item should now exist
    r_items = client.get("/action-items/")
    assert r_items.status_code == 200
    items = r_items.json()
    assert any(i["description"].lower() == "task1" for i in items)
