from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    profilepic = Column(String(255), nullable=True)
    name = Column(String(255), nullable=False)
    cellnumber = Column(String(20), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    deletedAt = Column(DateTime, nullable=True)
    created = Column(DateTime, server_default=func.now())
    modified = Column(DateTime, server_default=func.now(), onupdate=func.now())
    roleId = Column(Integer, nullable=False)  # 1: Admin, 2: Normal User

class AccessToken(Base):
    __tablename__ = "accesstoken"
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(255), unique=True, nullable=False)
    ttl = Column(Integer, nullable=False)  # time-to-live in ms
    userId = Column(Integer, ForeignKey("user.id"), nullable=False)
    created = Column(DateTime, server_default=func.now())
