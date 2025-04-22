from sqlalchemy.orm import Session
from models import User, UserDevice
import schemas
from fastapi import HTTPException

# ------------------- Users ----------------------

def create_user(db: Session, user: schemas.UserCreate):
    db_user = User(**user.dict())  # Convert Pydantic to SQLAlchemy
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

# ------------------- Devices ----------------------

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
