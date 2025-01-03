from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from uuid import uuid4
from database import users_collection
from utils.hashing import hash_password, verify_password
from utils.auth import create_access_token
from datetime import datetime
from utils.auth import decode_token
from datetime import timedelta

router = APIRouter()

class UserLogin(BaseModel):
    email_or_phone: str
    password: str

@router.post("/register/")
async def register_user(user: dict):
    user['user_id'] = str(uuid4())
    user['password'] = hash_password(user['password'])
    user['created_on'] = user['last_update'] = datetime.utcnow()

    existing_user = await users_collection.find_one({"user_email": user["user_email"]})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already in use")
    
    await users_collection.insert_one(user)
    return {"message": "User registered successfully"}

@router.post("/login/")
async def login(user: UserLogin):
    query = {"$or": [{"user_email": user.email_or_phone}, {"mobile_number": user.email_or_phone}]}
    db_user = await users_collection.find_one(query)
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"user_id": db_user["user_id"]}, timedelta(minutes=15))
    refresh_token = create_access_token({"user_id": db_user["user_id"]}, timedelta(days=30))
    return {"access_token": access_token, "refresh_token": refresh_token}
