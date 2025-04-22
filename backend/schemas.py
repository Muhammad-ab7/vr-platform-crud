from pydantic import BaseModel
from datetime import datetime

# ----- User Schemas -----
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True

# ----- UserDevice Schemas -----
class UserDeviceBase(BaseModel):
    device_type: str
    serial_number: str

class UserDeviceCreate(UserDeviceBase):
    user_id: int

class UserDeviceOut(UserDeviceBase):
    device_id: int
    user_id: int
    registered_at: datetime

    class Config:
        orm_mode = True
