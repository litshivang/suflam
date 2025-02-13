from sqlalchemy.orm import Session
from datetime import datetime
from .models import User, AccessToken
from .schemas import UserCreate, UserLogin
from .auth import hash_password, verify_password, generate_access_token
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

def create_user(db: Session, user: UserCreate):
    try:
        db_user = User(
            profilepic=user.profilepic,
            name=user.name,
            cellnumber=user.cellnumber,
            password=hash_password(user.password),
            email=user.email,
            roleId=user.roleId
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError as e:
        db.rollback()
        # Raise a clear error message for duplicate or constraint violation issues
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Integrity error: {e.orig}"
        )

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def update_user(db: Session, user_id: int, user_data: dict):
    user = get_user(db, user_id)
    if not user:
        return None
    for key, value in user_data.items():
        if key == "password":
            setattr(user, key, hash_password(value))
        else:
            setattr(user, key, value)
    user.modified = datetime.utcnow()
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    if not user:
        return None
    db.delete(user)
    db.commit()
    return user

def list_users(db: Session):
    return db.query(User).all()

def login_user(db: Session, login_data: UserLogin):
    user = db.query(User).filter(User.cellnumber == login_data.cellnumber).first()
    if not user or not verify_password(login_data.password, user.password):
        return None
    # Generate access token and store in DB
    token = generate_access_token()
    ttl = 30000  # e.g., 30,000 ms = 30 seconds
    access_token = AccessToken(token=token, ttl=ttl, userId=user.id)
    db.add(access_token)
    db.commit()
    db.refresh(access_token)
    return access_token
