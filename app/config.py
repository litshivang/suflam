import os
from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env if available

# Database configuration (update these or set in .env)
DATABASE_USER = os.getenv("DATABASE_USER", "chandresh")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "chandresh")
DATABASE_HOST = os.getenv("DATABASE_HOST", "192.168.1.223")
DATABASE_PORT = os.getenv("DATABASE_PORT", "3306")
DATABASE_NAME = os.getenv("DATABASE_NAME", "suflam")

SQLALCHEMY_DATABASE_URL = (
    f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
)
