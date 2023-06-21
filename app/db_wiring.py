from pydantic import EmailStr, BaseModel
from fastapi import FastAPI, Depends, HTTPException

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

import os

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

def get_user_by_email(db: Session, email: str):
    return db.query(UserDB).filter(UserDB.email == email).first()

def get_last_data(db: Session, email:str):
    return db.query(Paths).filter(UserDB.email == email).order_by(Paths.id.desc()).first()

#Endpoints
@api.post("/users/", response_model=UserOut)
def create_user(user: UserIn, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    if not os.path.exists(f"users/{user.email}"):
        os.mkdir(f"users/{user.email}")
    return create_user_db(db=db, user=user)
    
