from pydantic import EmailStr, BaseModel
from fastapi import FastAPI, Depends, HTTPException

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, DateTime
from sqlalchemy.orm import relationship

from typing import List

import os
import datetime

SQLALCHEMY_DATABASE_URL = "sqlite:///./app/db/eq_monitor.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

api = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Schema FastAPI
class UserOut(BaseModel):
    email: EmailStr
    
    class Config:
        orm_mode = True

class UserIn(UserOut):
    password: str

class DateOut(BaseModel):
    email: EmailStr
    path: str
    date_upload: datetime.date
    date_eq_start: datetime.datetime
    date_eq_end: datetime.datetime

    class Config:
        orm_mode = True

class DateIn(DateOut):
    data: List[DateOut]


#Model DB
class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    paths = relationship("Paths", back_populates = "users")

class Paths(Base):
    __tablename__ = "paths"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, ForeignKey("users.email"))
    path = Column(String, unique=True, index=True)
    date_upload = Column(Date)
    date_eq_start = Column(DateTime)
    date_eq_end = Column(DateTime)

    users = relationship("UserDB", back_populates = "paths")
    
Base.metadata.create_all(bind=engine)

#CRUD
def create_user_db(db: Session, user: UserIn):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = UserDB(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_path_db(db: Session, data: DateIn):
    db_path = Paths(email = data.email, path = data.path, date_upload = data.date_upload, date_eq_start = data.date_eq_start, data_eq_end = data.date_eq_end)
    db.add(db_path)
    db.commit()
    db.refresh(db_path)
    return db_path

def get_user_by_email(db: Session, email: str):
    return db.query(UserDB).filter(UserDB.email == email).first()

def get_path(db: Session, path: str):
    return db.query(Paths).filter(Paths.path == path).first()

def get_last_data(db: Session, email:str):
    return db.query(Paths).filter(UserDB.email == email).order_by(Paths.id.desc()).first()

def get_data_by_date(db: Session, email: str, date: datetime.date):
    db_user = get_user_by_email(db, email=email)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db.query(Paths).filter(Paths.email == db_user.email, Paths.date_eq_start == date).all()
# def get_data_by_interval(db: Session, email:str, data_eq_start: datetime.datetime, data_eq_end: datetime.datetime):
#     db_

#Endpoints
@api.post("/users/", response_model=UserOut)
def create_user(user: UserIn, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user_db(db=db, user=user)
@api.post("/users/", response_model=DateOut)
def create_path(data: DateIn):
    db_path = get_path(db, path = data.path)
    if db_path:
        raise HTTPException(status_code=400, detail="Path exists")
    return create_path_db(db=db, path=path)

@api.get("/users/{email}", response_model = DateOut)
def get_last_files(data: DateIn, db: Session = Depends(get_db)):
    data = get_last_data(db=db, email=email)
    if not data:
        raise HTTPException(status_code=404, detail="Jopa")
    return data
@api.get("/users/{email}/{date}", response_model=DateOut)
def get_files(data: DateIn, db: Session = Depends(get_db)):
    data = get_data_by_date(db=db, email=email, date=date)
    if not data:
        raise HTTPException(status_code=404, detail="Jopa")
    return data




    
