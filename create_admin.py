# create_admin.py
from app.database import SessionLocal
from app.crud import create_user
from app.schemas import UserCreate

db = SessionLocal()
admin_data = UserCreate(
    profilepic=None,
    name="Admin User",
    cellnumber="1234567890",
    password="AdminSecurePassword!",
    email="admin@example.com",
    roleId=1  # Admin Role
)
admin = create_user(db, admin_data)
print("Admin user created with ID:", admin.id)
db.close()
