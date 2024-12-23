from fastapi import HTTPException, Header, Depends
from .database import DatabaseSessionLocal
from sqlalchemy.orm import Session
from .crud import get_user_by_token


async def validate_token(authorization: str = Header(...)):
    """validate and use the token for protected routes"""
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")
    return authorization


def get_database():
    db = DatabaseSessionLocal()
    try:
        yield db
    finally:
        db.close()


async def check_role(role: str, token: str):
    """check if the user has the required role"""
    try:
        db = DatabaseSessionLocal()
        user = get_user_by_token(db, token)
    finally:
        db.close()
    if not user or user.role != role:
        raise HTTPException(
            status_code=403, detail="Access Forbidden, check your access token"
        )


async def check_if_user_role(token: str):
    return await check_role("user", token)


async def check_if_admin_role(token: str):
    return await check_role("admin", token)
