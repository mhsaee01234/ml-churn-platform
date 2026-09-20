from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "ML Churn Prediction API is running!"


def test_register_and_predict():
    username = "testuser"
    password = "testpass123"

    # Register test user
    register_response = client.post(
        "/register",
        json={
            "username": username,
            "password": password
        }
    )

    # User may already exist from an earlier test run
    assert register_response.status_code in [200, 400]

    # Login
    login_response = client.post(
        "/login",
        json={
            "username": username,
            "password": password
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    # Make authenticated prediction request
    response = client.post(
        "/predict",
        json={
            "features": [12, 70.5, 850.0]
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert "prediction" in response.json()
    assert "saved_id" in response.json()