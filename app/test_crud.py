import pytest
from loguru import logger
from .database import SessionLocal
from .models import UserDB
from .schemas import UserIn

from .crud import generate_token, create_user_db, create_path_db



def test_generate_token():
    token = generate_token()

    # Проверяем, что токен был сгенерирован
    assert token is not None

    # Проверяем, что токен имеет правильную длину
    assert len(token) == 32

@pytest.fixture(scope="module")
def test_db():
    # Настройка тестовой базы данных
    db = SessionLocal()
    yield db
    db.close()

@pytest.fixture(autouse=True)
def cleanup_test_db(test_db):
    # Очистка базы данных после выполнения каждого теста
    test_db.query(UserDB).delete()
    test_db.commit()

def test_create_user_db(test_db, caplog):
    # Перехватываем вывод в журнал
    caplog.set_level("INFO")

    # Создаем тестового пользователя
    user = UserIn(email="test5@example.com", password="password")
    created_user = create_user_db(test_db, user)

    # Проверяем, что пользователь был создан
    assert created_user is not None

    # Проверяем, что у пользователя есть токен
    assert created_user.token is not None
