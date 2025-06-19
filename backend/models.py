from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default="user")  # can be "admin" or "user"
    created_at = Column(DateTime, default=datetime.utcnow)

class UserDevice(Base):
    __tablename__ = "user_devices"

    device_id = Column(Integer, primary_key=True, index=True)
    device_type = Column(String, nullable=False)
    serial_number = Column(String, unique=True, nullable=False)
    registered_at = Column(DateTime, default=datetime.utcnow)