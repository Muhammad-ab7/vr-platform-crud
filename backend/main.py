from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import User, UserDevice
from database import SessionLocal
import crud
import schemas 
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users", response_model=list[schemas.UserOut])
def read_users(db: Session = Depends(get_db)):
    return crud.get_users(db)

@app.post("/users", response_model=schemas.UserOut)
def add_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@app.put("/users/{user_id}", response_model=schemas.UserOut)
def edit_user(user_id: int, user: schemas.UserBase, db: Session = Depends(get_db)):
    return crud.update_user(db, user_id, user)

@app.delete("/users/{user_id}")
def remove_user(user_id: int, db: Session = Depends(get_db)):
    crud.delete_user(db, user_id)
    return {"message": "User deleted"}

@app.get("/devices", response_model=list[schemas.UserDeviceOut])
def read_devices(db: Session = Depends(get_db)):
    return crud.get_devices(db)

@app.post("/devices", response_model=schemas.UserDeviceOut)
def add_device(device: schemas.UserDeviceCreate, db: Session = Depends(get_db)):
    return crud.create_device(db, device)

@app.put("/devices/{device_id}", response_model=schemas.UserDeviceOut)
def edit_device(device_id: int, device: schemas.UserDeviceBase, db: Session = Depends(get_db)):
    return crud.update_device(db, device_id, device)

@app.delete("/devices/{device_id}")
def remove_device(device_id: int, db: Session = Depends(get_db)):
    crud.delete_device(db, device_id)
    return {"message": "Device deleted"}

@app.post("/login")
def login(credentials: schemas.LoginRequest, db: Session = Depends(get_db)):
    return crud.verify_user_login(db, credentials.username, credentials.password)

@app.post("/signup", response_model=dict)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    crud.create_user(db, user)
    return {"message": "Signup successful"}
