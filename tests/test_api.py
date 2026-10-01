from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


def get_token():
    response = client.post(
        "/auth/login",
        data={
            "username": "admin",
            "password": "admin123",
        },
    )

    assert response.status_code == 200

    return response.json()["access_token"]


def test_login():
    response = client.post(
        "/auth/login",
        data={
            "username": "admin",
            "password": "admin123",
        },
    )

    assert response.status_code == 200
    assert "access_token" in response.json()


def test_auth_me():
    token = get_token()

    response = client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200
    assert response.json()["username"] == "admin"


def test_claims_dashboard():
    token = get_token()

    response = client.get(
        "/claims/dashboard",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200


def test_data_quality():
    token = get_token()

    response = client.get(
        "/data-quality/",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200
    assert response.json()["quality_score"] == 100


def test_fraud_detection():
    token = get_token()

    response = client.get(
        "/fraud-detection/",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200