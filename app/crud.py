from .database import *
from .models import *
from .schemas import *

def create_user_db(db: Session, user: UserIn):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = UserDB(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_path_db(db: Session,email: EmailStr, path:str, date_upload: str, date_eq_start: str, date_eq_end: str):
    db_path = PathsDB(email = email, path = path, date_upload = date_upload, date_eq_start = date_eq_start, date_eq_end = date_eq_end)
    db.add(db_path)
    db.commit()
    db.refresh(db_path)
    return db_path

def get_user_by_email(db: Session, email: str):
    return db.query(UserDB).filter(UserDB.email == email).first()

def get_path(db: Session, path: str):
    return db.query(PathsDB).filter(PathsDB.path == path).first()

def get_last_data(db: Session, email:str):
    date_upload =  db.query(PathsDB).filter(UserDB.email == email).order_by(PathsDB.id.desc()).first().date_upload
    return db.query(PathsDB).filter(UserDB.email == email, PathsDB.date_upload == date_upload).all()

def get_data_by_date(db: Session, email: str, date: str):
    db_user = get_user_by_email(db, email=email)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db.query(PathsDB).filter(PathsDB.email == email, PathsDB.date_eq_start.contains(date)).all()