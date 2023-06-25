from loguru import logger

from .database import *
from .models import *
from .schemas import *

import secrets

def generate_token():
    token = secrets.token_hex(16) 
    logger.info(f"Generated token: {token}")
    return token

def create_user_db(db: Session, user: UserToken):
    fake_hashed_password = user.password + "notreallyhashed"
    token = generate_token()
    db_user = UserDB(email=user.email, hashed_password=fake_hashed_password, token=token)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f"User created: {user.token}")
    return db_user

def create_path_db(db: Session,email: EmailStr, path:str, date_upload: str, date_eq_start: str, date_eq_end: str):
    user = get_user_by_email(db=db, email=email)
    db_path = PathsDB(email = email, path = path, date_upload = date_upload, date_eq_start = date_eq_start, date_eq_end = date_eq_end)
    db.add(db_path)
    db.commit()
    db.refresh(db_path)
    logger.info(f"Path created for user: {user.token}")
    return db_path

def get_user_by_email(db: Session, email: str):
    logger.info(f"Getting user by email")
    return db.query(UserDB).filter(UserDB.email == email).first()

def get_path(db: Session, path: str):
    logger.info(f"Getting path")
    return db.query(PathsDB).filter(PathsDB.path == path).first()

def get_last_data(db: Session, email:str):
    user = get_user_by_email(db=db, email=email)
    logger.info(f"Getting last data for user: {user.token}")
    date_upload =  db.query(PathsDB).filter(UserDB.email == email).order_by(PathsDB.id.desc()).first().date_upload
    data = db.query(PathsDB).filter(UserDB.email == email, PathsDB.date_upload == date_upload).all()
    logger.info(f"Last data retrieved for user: {user.token}")
    return data

def get_data_by_date(db: Session, email: str, date: str):
    user = get_user_by_email(db, email=email)
    logger.info(f"Getting data for user: {user.token}, date: {date}")
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    data = db.query(PathsDB).filter(PathsDB.email == email, PathsDB.date_eq_start.contains(date)).all()
    logger.info(f"Data retrieved for user: {user.token}, date: {date}")
    return data