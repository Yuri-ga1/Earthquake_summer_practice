from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, DateTime
from sqlalchemy.orm import relationship
from .database import *

class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    paths = relationship("PathsDB", back_populates = "users")

class PathsDB(Base):
    __tablename__ = "paths"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, ForeignKey("users.email"))
    path = Column(String, index=True)
    date_upload = Column(String)
    date_eq_start = Column(String)
    date_eq_end = Column(String)
    users = relationship("UserDB", back_populates = "paths")

Base.metadata.create_all(bind=engine)