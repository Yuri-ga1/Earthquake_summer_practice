import pytest
from fastapi.testclient import TestClient
from .database import *
from .main import *

# Создание тестового клиента
client = TestClient(api)

def test_get_db():
    with get_db() as db:
        # Проверка, что функция get_db возвращает объект базы данных
        assert db is not None
