from fastapi.testclient import TestClient

from background_removal.api import app


client = TestClient(app)


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_remove_endpoint(monkeypatch):
    def fake_remove_background(data: bytes, model: str = "u2net") -> bytes:  # pragma: no cover - simple stub
        return b"PNGDATA"

    monkeypatch.setattr("background_removal.service.remove_background", fake_remove_background)

    files = {"file": ("test.png", b"bytes", "image/png")}
    response = client.post("/api/remove", files=files)

    assert response.status_code == 200
    assert response.content == b"PNGDATA"
    assert response.headers["content-type"] == "image/png"
