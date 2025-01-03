from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime

# User Model
class User(BaseModel):
    user_id: UUID
    user_name: str
    user_email: EmailStr
    mobile_number: str
    password: str
    created_on: datetime
    last_update: datetime

# Note Model
class Note(BaseModel):
    note_id: UUID
    user_id: UUID
    note_title: str
    note_content: str
    created_on: datetime
    last_update: datetime
