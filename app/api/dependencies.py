from fastapi import HTTPException, Header, Depends
from .database import Admin, DatabaseSessionLocal, User
from sqlalchemy.orm import Session
from .crud import get_user_by_token, get_database, get_user_by_id, get_admin_by_id


async def validate_token(authorization: str = Header(...)):
    """validate and use the token for protected routes"""
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")
    return authorization


async def validate_user_id(user_id: int):
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user_id


async def validate_admin_id(user_id: int):
    user = get_admin_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Admin not found")
    return user_id


async def check_role(role: str, token: str):
    """check if the user has the required role"""
    try:
        db = DatabaseSessionLocal()
        instance = User if role == "user" else Admin
        user = get_user_by_token(token, instance)
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
