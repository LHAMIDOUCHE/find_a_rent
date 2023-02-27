from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_wrong_body():
    response = client.post("/search")
    assert response.status_code == 422
    assert "detail" in response.json()


def test_make_request_with_apropriate_department():
    response = client.post(
        "/search", json={"department": "95", "surface": 80, "maximum_rent_price": 300}
    )
    assert response.status_code == 200


def test_make_request_with_not_existing_department():
    response = client.post(
        "/search", json={"department": "9D3", "surface": 80, "maximum_rent_price": 300}
    )
    assert response.status_code == 404
