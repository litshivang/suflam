from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# User Schemas
class UserCreate(BaseModel):
    profilepic: Optional[str] = None
    name: str
    cellnumber: str
    password: str
    email: EmailStr
    roleId: int  # 1 for Admin, 2 for Normal User

class UserResponse(BaseModel):
    id: int
    profilepic: Optional[str]
    name: str
    cellnumber: str
    email: EmailStr
    roleId: int
    created: datetime
    modified: datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    cellnumber: str
    password: str

# Token Schema
class TokenResponse(BaseModel):
    token: str
    ttl: int
    userId: int
    created: datetime

    class Config:
        from_attributes = True
