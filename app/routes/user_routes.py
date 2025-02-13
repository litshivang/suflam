from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..schemas import UserCreate, UserResponse, UserLogin, TokenResponse
from .. import crud
from ..auth import get_db, admin_required, get_current_user

router = APIRouter(prefix="/api/users", tags=["users"])

# --- Admin-only Endpoints ---

@router.post("/", response_model=UserResponse, dependencies=[Depends(admin_required)])
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@router.patch("/{user_id}", response_model=UserResponse, dependencies=[Depends(admin_required)])
def update_existing_user(user_id: int, user_data: dict, db: Session = Depends(get_db)):
    updated = crud.update_user(db, user_id, user_data)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return updated

@router.delete("/{user_id}", dependencies=[Depends(admin_required)])
def delete_existing_user(user_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_user(db, user_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"detail": "User deleted successfully"}

@router.get("/", response_model=List[UserResponse], dependencies=[Depends(admin_required)])
def list_all_users(db: Session = Depends(get_db)):
    return crud.list_users(db)

# --- Endpoint Accessible by Both Admin and User (GET /{id}) ---
@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    # Normal users can view only their own data
    if current_user.roleId != 1 and current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden")
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

# --- Login Endpoint (accessible by any user) ---
@router.post("/login", response_model=TokenResponse)
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    token_obj = crud.login_user(db, login_data)
    if not token_obj:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return token_obj
