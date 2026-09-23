from fastapi.testclient import TestClient

from app.main import create_app


def test_waitlist_flow_and_persistence(tmp_path):
    url = f"sqlite:///{tmp_path / 'parties.db'}"
    client = TestClient(create_app(url))
    first = client.post("/api/parties", json={"name": "  Alex  ", "size": 2})
    second = client.post("/api/parties", json={"name": "Sam", "size": 4})
    assert first.status_code == second.status_code == 201
    assert first.json()["name"] == "Alex"
    assert [p["name"] for p in client.get("/api/parties?status=waiting").json()] == ["Alex", "Sam"]

    party_id = first.json()["id"]
    assert client.patch(f"/api/parties/{party_id}", json={"status": "seated"}).status_code == 200
    assert [p["name"] for p in client.get("/api/parties?status=waiting").json()] == ["Sam"]
    assert client.patch(f"/api/parties/{party_id}", json={"status": "removed"}).status_code == 409

    restarted = TestClient(create_app(url))
    assert restarted.get("/api/parties?status=seated").json()[0]["name"] == "Alex"
    assert restarted.get("/api/parties?status=waiting").json()[0]["name"] == "Sam"


def test_validation_and_missing_party(tmp_path):
    client = TestClient(create_app(f"sqlite:///{tmp_path / 'validation.db'}"))
    for payload in ({"name": "  ", "size": 2}, {"name": "A", "size": 0}, {"name": "A", "size": 21}, {"name": "A", "size": True}, {"name": "A" * 81, "size": 2}):
        assert client.post("/api/parties", json=payload).status_code == 422
    assert client.get("/api/parties").json() == []
    assert client.patch("/api/parties/999", json={"status": "seated"}).status_code == 404
