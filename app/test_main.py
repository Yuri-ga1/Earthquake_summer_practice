import pytest
from fastapi.testclient import TestClient
from .main import api

# Создание тестового клиента
client = TestClient(api)

def test_create_user_true(email = "user12@example.com"):
    response = client.post("/users/",
                           json={"email" : email, "password" : "12345678"})
    assert response.status_code == 200
    assert response.json() == {
        "email" : email
    }

def test_create_user_fail():
    response = client.post("/users/",
                           json={"email" : "user@example.com", "password" : "12345678"})
    assert response.status_code == 400
    assert response.json() == {"detail" : "Email already registered"}

def test_get_files_by_date_true(email="user@example.com", date="2023-12-12"):
    response = client.get(f"get_files/{email}/{date}", headers={"email" : email, "date" : date})
    assert response.status_code == 200

def test_get_files_by_date_false_user(email="123456@example.com", date="2023-12-12"):
    response = client.get(f"get_files/{email}/{date}", headers={"email" : email, "date" : date})
    assert response.status_code == 404
    assert response.json() == {"detail" : "User not found"}

def test_get_last_upload_true(email="user@example.com"):
    response = client.get(f"get_last_upload/{email}", headers={"email" : email})
    assert response.status_code == 200

def test_get_files_by_date_false_user(email="123456@example.com"):
    response = client.get(f"get_last_upload/{email}", headers={"email" : email})
    assert response.status_code == 404
    assert response.json() == {"detail" : "User not found"}

#
#def test_upload_files_true():
#    response = client.post("/upload_files",
#                json={"email" : "user@example.com", 
#                      "date_eq_start": "2022-12-12 05:05:05",
#                      "date_eq_end": "2022-12-13 05:05:05"})
#    print(response.json())
#    assert response.status_code == 200
#    assert response.json() == {"Message" : "Successfull"}
#
#def test_upload_files_future_date():
#    response = client.post("/upload_files",
#                json={"email" : "user@example.com", 
#                      "date_eq_start": "9999-12-12 05:05:05",
#                      "date_eq_end": "9999-12-12 06:05:05"})
#    assert response.status_code == 400
#    assert response.json() == {"detail" : "Earthquake start date cann't be in the future"}
#
#def test_upload_files_date_of_beginning_later_than_end():
#    response = client.post("/upload_files",
#                json={"email" : "user@example.com", 
#                      "date_eq_start": "9999-12-12 05:05:05",
#                      "date_eq_end": "2022-12-13 05:05:05"})
#    assert response.status_code == 400
#    assert response.json() == {"detail" : "The date of the beginning of the earthquake cannot be later than the end"}
#