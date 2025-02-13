from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from app.database import engine
from app.models import Base
from app.routes import user_routes

app = FastAPI(title="User Management API")

# Global handler for SQLAlchemy IntegrityError (e.g., duplicate mobile number)
@app.exception_handler(IntegrityError)
async def integrity_exception_handler(request: Request, exc: IntegrityError):
    # Rollback is done in the CRUD functions; this returns a clear error message
    return JSONResponse(
        status_code=400,
        content={"detail": f"Database integrity error: {exc.orig}"}
    )

# Generic handler for all unhandled exceptions
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    # Allow HTTPExceptions to pass through
    if isinstance(exc, HTTPException):
        raise exc
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {exc}"}
    )

# Create database tables on startup
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# Include API routes
app.include_router(user_routes.router)
