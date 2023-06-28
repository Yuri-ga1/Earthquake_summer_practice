import pytest
from fastapi.testclient import TestClient
from .main import api

# Создание тестового клиента
client = TestClient(api)

def test_create_user_true():
    response = client.post("/users/",
                           json={"email" : "user123456@example.com", "password" : "12345678"})
    assert response.status_code == 200
    assert response.json() == {
        "email" : "user12345@example.com"
    }

def test_create_user_fail():
    response = client.post("/users/",
                           json={"email" : "user12345@example.com", "password" : "12345678"})
    assert response.status_code == 400
    assert response.json() == {
        "email" : "user123456@example.com"
    }

def test_upload_files_true():
    response = client.post("/upload_files",
                json={"email" : "user@example.com", 
                      "date_eq_start": "2022-12-12 05:05:05",
                      "date_eq_end": "2022-12-13 05:05:05"})
    assert response.status_code == 200
    assert response.json() == {"Message" : "Successfull"}

def test_upload_files_future_date():
    response = client.post("/upload_files",
                json={"email" : "user@example.com", 
                      "date_eq_start": "9999-12-12 05:05:05",
                      "date_eq_end": "2022-12-13 05:05:05"})
    assert response.status_code == 400

def test_get_files_by_date_true():
    #response = client.get("email" : "user@example.com", "date" : "2023-12-12")
    pass