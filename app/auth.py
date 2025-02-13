from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import datetime
import secrets

from .database import SessionLocal
from .models import User, AccessToken

# Password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def generate_access_token() -> str:
    # Generate a secure random token string
    return secrets.token_urlsafe(32)

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency to get current user from token
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    token_record = db.query(AccessToken).filter(AccessToken.token == token).first()
    if not token_record:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    token_age = (datetime.utcnow() - token_record.created).total_seconds() * 1000  # in ms
    if token_age > token_record.ttl:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    
    user = db.query(User).filter(User.id == token_record.userId).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user

# Dependency to ensure current user is admin
def admin_required(current_user: User = Depends(get_current_user)):
    if current_user.roleId != 1:  # 1 = Admin
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return current_user
