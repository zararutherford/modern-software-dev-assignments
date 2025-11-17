def test_create_and_list_tags(client):
    payload = {"name": "important"}
    r = client.post("/tags/", json=payload)
    assert r.status_code == 201, r.text
    tag = r.json()
    assert tag["name"] == "important"
    assert "created_at" in tag and "updated_at" in tag

    r = client.get("/tags/")
    assert r.status_code == 200
    tags = r.json()
    assert len(tags) >= 1


def test_create_duplicate_tag(client):
    payload = {"name": "urgent"}
    r = client.post("/tags/", json=payload)
    assert r.status_code == 201

    r = client.post("/tags/", json=payload)
    assert r.status_code == 400


def test_delete_tag(client):
    payload = {"name": "temp"}
    r = client.post("/tags/", json=payload)
    assert r.status_code == 201
    tag_id = r.json()["id"]

    r = client.delete(f"/tags/{tag_id}")
    assert r.status_code == 204

    r = client.get(f"/tags/{tag_id}")
    assert r.status_code == 404


def test_add_and_remove_tag_from_note(client):
    # Create a note
    note_payload = {"title": "Tagged Note", "content": "This note has tags"}
    r = client.post("/notes/", json=note_payload)
    assert r.status_code == 201
    note_id = r.json()["id"]

    # Create a tag
    tag_payload = {"name": "project"}
    r = client.post("/tags/", json=tag_payload)
    assert r.status_code == 201
    tag_id = r.json()["id"]

    # Add tag to note
    r = client.post(f"/tags/{tag_id}/notes/{note_id}")
    assert r.status_code == 204

    # Remove tag from note
    r = client.delete(f"/tags/{tag_id}/notes/{note_id}")
    assert r.status_code == 204


def test_validation_empty_tag_name(client):
    payload = {"name": ""}
    r = client.post("/tags/", json=payload)
    assert r.status_code == 422
