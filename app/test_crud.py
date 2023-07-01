import pytest
from loguru import logger
from .database import SessionLocal
from .models import UserDB
from .schemas import UserIn
from .crud import * 

def test_generate_token():
    token = generate_token()

    assert token is not None
    assert len(token) == 32

@pytest.fixture(scope="module")
def test_db():
    db = SessionLocal()
    yield db
    db.close()

@pytest.fixture(autouse=True)
def cleanup_test_db(test_db):
    test_db.query(UserDB).delete()
    test_db.commit()

def test_create_user_db(test_db, caplog):
    caplog.set_level("INFO")

    user_data = UserIn(email="test@example.com", password="password")
    created_user = create_user_db(test_db, user_data)
    
    assert created_user is not None
    assert created_user.token is not None
    assert created_user.email == "test@example.com"
    assert created_user.hashed_password == "passwordnotreallyhashed"

def test_create_path_db(test_db, caplog):
    caplog.set_level("INFO")

    email = "test@example.com"
    path = "/test/path"
    date_upload = "2023-06-27"
    date_eq_start = "2023-06-01"
    date_eq_end = "2023-06-30"

    user_data = UserIn(email="test@example.com", password="password")
    user = create_user_db(test_db, user_data)
    created_path = create_path_db(
        db=test_db,
        email=email,
        path=path,
        date_upload=date_upload,
        date_eq_start=date_eq_start,
        date_eq_end=date_eq_end,
    )

    assert created_path is not None
    assert created_path.email == "test@example.com"
    assert created_path.path == "/test/path"
    assert created_path.date_upload == "2023-06-27"
    assert created_path.date_eq_start == "2023-06-01"
    assert created_path.date_eq_end == "2023-06-30"

def test_get_user_by_email(test_db, caplog):
    caplog.set_level("INFO")

    user = UserDB(email="test@example.com", hashed_password="password", token=generate_token())
    test_db.add(user)
    test_db.commit()

    retrieved_user = get_user_by_email(test_db, email="test@example.com")

    assert retrieved_user.email == "test@example.com"
    assert retrieved_user.hashed_password == "password"

def test_get_path(test_db, caplog):
    caplog.set_level("INFO")
     
    email = "test@example.com"
    path = "/test/path"
    date_upload = "2023-06-27"
    date_eq_start = "2023-06-01"
    date_eq_end = "2023-06-30"

    
    user_data = UserIn(email="test@example.com", password="password")
    user = create_user_db(test_db, user_data)
    created_path = create_path_db(
        db=test_db,
        email=email,
        path=path,
        date_upload=date_upload,
        date_eq_start=date_eq_start,
        date_eq_end=date_eq_end,
    )

    retrieved_path = get_path(test_db, path="/test/path")

    assert retrieved_path is not None
    assert retrieved_path.email == "test@example.com"
    assert retrieved_path.path == "/test/path"
    assert retrieved_path.date_upload == "2023-06-27"
    assert retrieved_path.date_eq_start == "2023-06-01"
    assert retrieved_path.date_eq_end == "2023-06-30"

def test_get_last_data(test_db, caplog):
    caplog.set_level("INFO")
    
    email = "test@example.com"
    path1 = "/test/path1"
    path2 = "/test/path2"
    date_upload1 = "2023-06-27"
    date_upload2 = "2023-06-21"
    date_eq_start = "2023-06-01"
    date_eq_end = "2023-06-30"

    user_data = UserIn(email="test@example.com", password="password")
    user = create_user_db(test_db, user_data)
    created_path = create_path_db(
        db=test_db,
        email=email,
        path=path1,
        date_upload=date_upload1,
        date_eq_start=date_eq_start,
        date_eq_end=date_eq_end,
    )
    created_path = create_path_db(
        db=test_db,
        email=email,
        path=path2,
        date_upload=date_upload2,
        date_eq_start=date_eq_start,
        date_eq_end=date_eq_end,
    )

    retrieved_data = get_last_data(test_db, email="test@example.com")

    assert retrieved_data is not None
    assert len(retrieved_data) > 0
    assert retrieved_data[0].email == "test@example.com"
    assert retrieved_data[0].date_upload == "2023-06-21"

def test_get_data_by_date(test_db, caplog):
    caplog.set_level("INFO")
    
    email = "test@example.com"
    path = "/test/path"
    date_upload = "2023-06-27"
    date_eq_start = "2023-06-01"
    date_eq_end = "2023-06-30"

    user_data = UserIn(email="test@example.com", password="password")
    user = create_user_db(test_db, user_data)
    created_path = create_path_db(
        db=test_db,
        email=email,
        path=path,
        date_upload=date_upload,
        date_eq_start=date_eq_start,
        date_eq_end=date_eq_end,
    )

    retrieved_data = get_data_by_date(test_db, email="test@example.com", date="2023-06-01")

    assert retrieved_data is not None
    assert len(retrieved_data) > 0
    assert retrieved_data[0].email == "test@example.com"
    assert retrieved_data[0].date_eq_start == "2023-06-01"