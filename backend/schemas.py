from pydantic import BaseModel
from datetime import datetime

# ----- User Schemas -----
class UserBase(BaseModel):
    username: str
    email: str

class UserOut(UserBase):
    user_id: int
    role: str  # add this

    class Config:
        orm_mode = True

class UserCreate(UserBase):
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

# ----- UserDevice Schemas -----
class UserDeviceBase(BaseModel):
    device_type: str
    serial_number: str

class UserDeviceCreate(UserDeviceBase):
      pass

class UserDeviceOut(UserDeviceBase):
    device_id: int
    device_type: str
    serial_number: str
    registered_at: datetime

    class Config:
        orm_mode = True

