from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, DateTime
from sqlalchemy.orm import relationship
from .database import *

class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    token = Column(String)

    paths = relationship("PathsDB", back_populates = "users")
    results = relationship("ResultDB", back_populates = "users")

class PathsDB(Base):
    __tablename__ = "paths"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, ForeignKey("users.email"))
    filename = Column(String)
    path = Column(String, index=True)
    date_upload = Column(String)
    date_eq_start = Column(String)
    date_eq_end = Column(String)

    users = relationship("UserDB", back_populates = "paths")
    results = relationship("ResultDB", back_populates = "paths")

class ResultDB(Base):
    __tablename__ = "results"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, ForeignKey("users.email"))
    filename = Column(String, ForeignKey("paths.filename"))
    path = Column(String, index=True)

    users = relationship("UserDB", back_populates = "results")
    paths = relationship("PathsDB", back_populates = "results")

Base.metadata.create_all(bind=engine)