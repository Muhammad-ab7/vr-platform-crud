from sqlalchemy.orm import Session
from models import User, UserDevice
import schemas
from fastapi import HTTPException
from passlib.context import CryptContext


def create_user(db: Session, user: schemas.UserCreate):
    # Check if username or email already exists
    existing = db.query(User).filter((User.username == user.username) | (User.email == user.email)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username or email already exists")
    
    # Hardcode one user as admin
    if user.username == "admin" or user.email == "admin@gmail.com":
        role = "admin"
    else:
        role = "user"

    hashed_password = pwd_context.hash(user.password)
    db_user = User(username=user.username, email=user.email, password=hashed_password, role=role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session):
    return db.query(User).all()

def update_user(db: Session, user_id: int, new_data: schemas.UserBase):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in new_data.dict(exclude_unset=True).items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()

def create_device(db: Session, device: schemas.UserDeviceCreate):
    db_device = UserDevice(**device.dict())
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device

def get_devices(db: Session):
    return db.query(UserDevice).all()

def update_device(db: Session, device_id: int, new_data: schemas.UserDeviceBase):
    device = db.query(UserDevice).filter(UserDevice.device_id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    for key, value in new_data.dict(exclude_unset=True).items():
        setattr(device, key, value)
    db.commit()
    db.refresh(device)
    return device

def delete_device(db: Session, device_id: int):
    device = db.query(UserDevice).filter(UserDevice.device_id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    db.delete(device)
    db.commit()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def verify_user_login(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    # Return all relevant user info
    return {
        "user_id": user.user_id,
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "created_at": user.created_at.isoformat()
    }

def get_user_by_email_or_username(db: Session, email: str, username: str):
    return db.query(User).filter((User.email == email) | (User.username == username)).first()

