import pytest
from fastapi.testclient import TestClient
from .main import api

# Создание тестового клиента
client = TestClient(api)

def test_create_user_true():
    response = client.post("/users/",
                           json={"email" : "user@example.com", "password" : "12345678"})
    assert response.status_code == 200
    assert response.json() == {
        "email" : "user@example.com"
    }
