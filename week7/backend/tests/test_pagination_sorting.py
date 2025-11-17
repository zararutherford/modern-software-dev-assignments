def test_notes_pagination(client):
    # Create multiple notes
    for i in range(15):
        payload = {"title": f"Note {i}", "content": f"Content {i}"}
        r = client.post("/notes/", json=payload)
        assert r.status_code == 201

    # Test default pagination
    r = client.get("/notes/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 15

    # Test with limit
    r = client.get("/notes/", params={"limit": 5})
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 5

    # Test with skip
    r = client.get("/notes/", params={"skip": 10, "limit": 5})
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 5

    # Test with skip beyond available items
    r = client.get("/notes/", params={"skip": 1000, "limit": 10})
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 0


def test_notes_sorting(client):
    # Create notes with different titles
    titles = ["Zebra", "Apple", "Mango"]
    created_ids = []
    for title in titles:
        payload = {"title": title, "content": "Test content"}
        r = client.post("/notes/", json=payload)
        assert r.status_code == 201
        created_ids.append(r.json()["id"])

    # Test ascending sort by title
    r = client.get("/notes/", params={"sort": "title", "limit": 100})
    assert r.status_code == 200
    items = r.json()
    # Find our created items
    our_items = [item for item in items if item["id"] in created_ids]
    assert len(our_items) == 3
    assert our_items[0]["title"] == "Apple"
    assert our_items[1]["title"] == "Mango"
    assert our_items[2]["title"] == "Zebra"

    # Test descending sort by title
    r = client.get("/notes/", params={"sort": "-title", "limit": 100})
    assert r.status_code == 200
    items = r.json()
    our_items = [item for item in items if item["id"] in created_ids]
    assert len(our_items) == 3
    assert our_items[0]["title"] == "Zebra"
    assert our_items[1]["title"] == "Mango"
    assert our_items[2]["title"] == "Apple"

    # Test sort by created_at (default)
    r = client.get("/notes/", params={"sort": "-created_at"})
    assert r.status_code == 200


def test_notes_sorting_by_id(client):
    # Create notes
    ids = []
    for i in range(3):
        payload = {"title": f"Note {i}", "content": "Content"}
        r = client.post("/notes/", json=payload)
        assert r.status_code == 201
        ids.append(r.json()["id"])

    # Test ascending sort by id
    r = client.get("/notes/", params={"sort": "id", "limit": 100})
    assert r.status_code == 200
    items = r.json()
    our_items = [item for item in items if item["id"] in ids]
    for i in range(len(our_items) - 1):
        assert our_items[i]["id"] < our_items[i + 1]["id"]

    # Test descending sort by id
    r = client.get("/notes/", params={"sort": "-id", "limit": 100})
    assert r.status_code == 200
    items = r.json()
    our_items = [item for item in items if item["id"] in ids]
    for i in range(len(our_items) - 1):
        assert our_items[i]["id"] > our_items[i + 1]["id"]


def test_notes_invalid_sort_field(client):
    # Invalid sort field should fall back to default
    r = client.get("/notes/", params={"sort": "invalid_field"})
    assert r.status_code == 200


def test_action_items_pagination(client):
    # Create multiple action items
    for i in range(12):
        payload = {"description": f"Task {i}"}
        r = client.post("/action-items/", json=payload)
        assert r.status_code == 201

    # Test with limit
    r = client.get("/action-items/", params={"limit": 5})
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 5

    # Test with skip
    r = client.get("/action-items/", params={"skip": 5, "limit": 5})
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 5

    # Test with skip and limit beyond available
    r = client.get("/action-items/", params={"skip": 100, "limit": 10})
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 0


def test_action_items_sorting(client):
    # Create action items
    descriptions = ["Zebra task", "Apple task", "Mango task"]
    created_ids = []
    for desc in descriptions:
        payload = {"description": desc}
        r = client.post("/action-items/", json=payload)
        assert r.status_code == 201
        created_ids.append(r.json()["id"])

    # Test ascending sort by description
    r = client.get("/action-items/", params={"sort": "description", "limit": 100})
    assert r.status_code == 200
    items = r.json()
    our_items = [item for item in items if item["id"] in created_ids]
    assert len(our_items) == 3
    assert our_items[0]["description"] == "Apple task"
    assert our_items[1]["description"] == "Mango task"
    assert our_items[2]["description"] == "Zebra task"

    # Test descending sort by created_at
    r = client.get("/action-items/", params={"sort": "-created_at"})
    assert r.status_code == 200


def test_action_items_filter_with_pagination(client):
    # Create completed and uncompleted items
    for i in range(10):
        payload = {"description": f"Task {i}"}
        r = client.post("/action-items/", json=payload)
        assert r.status_code == 201
        if i % 2 == 0:
            item_id = r.json()["id"]
            client.put(f"/action-items/{item_id}/complete")

    # Test filter with pagination
    r = client.get("/action-items/", params={"completed": True, "limit": 3})
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 3
    assert all(item["completed"] for item in items)

    r = client.get("/action-items/", params={"completed": False, "limit": 3})
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 3
    assert all(not item["completed"] for item in items)


def test_tags_pagination_and_sorting(client):
    # Create multiple tags
    tag_names = ["urgent", "important", "later", "archived"]
    for name in tag_names:
        payload = {"name": name}
        r = client.post("/tags/", json=payload)
        assert r.status_code == 201

    # Test pagination
    r = client.get("/tags/", params={"limit": 2})
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 2

    # Test sorting by name ascending
    r = client.get("/tags/", params={"sort": "name", "limit": 10})
    assert r.status_code == 200
    items = r.json()
    tag_items = [item for item in items if item["name"] in tag_names]
    assert len(tag_items) == 4
    assert tag_items[0]["name"] == "archived"
    assert tag_items[1]["name"] == "important"
    assert tag_items[2]["name"] == "later"
    assert tag_items[3]["name"] == "urgent"


def test_limit_boundary_conditions(client):
    # Test limit at maximum (200)
    r = client.get("/notes/", params={"limit": 200})
    assert r.status_code == 200

    # Test limit beyond maximum (should be capped at 200)
    r = client.get("/notes/", params={"limit": 500})
    assert r.status_code == 422  # Validation error

    # Test limit at 0
    r = client.get("/notes/", params={"limit": 0})
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 0
