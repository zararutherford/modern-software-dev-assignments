def test_create_and_list_notes(client):
    payload = {"title": "Test", "content": "Hello world"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["title"] == "Test"

    r = client.get("/notes/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1


def test_search_pagination_and_sort(client):
    # Ensure multiple notes
    for i in range(5):
        client.post("/notes/", json={"title": f"A{i}", "content": f"c{i}"})
    # Search with pagination
    r = client.get(
        "/notes/search/", params={"q": "A", "page": 1, "page_size": 2, "sort": "title_asc"}
    )
    assert r.status_code == 200
    data = r.json()
    assert set(data.keys()) == {"items", "total", "page", "page_size"}
    assert data["page"] == 1 and data["page_size"] == 2
    assert data["total"] >= 5
    assert len(data["items"]) == 2
    titles = [n["title"] for n in data["items"]]
    assert titles == sorted(titles)

    # Next page
    r2 = client.get(
        "/notes/search/", params={"q": "A", "page": 2, "page_size": 2, "sort": "title_asc"}
    )
    assert r2.status_code == 200
    data2 = r2.json()
    assert data2["page"] == 2
    assert len(data2["items"]) >= 1
