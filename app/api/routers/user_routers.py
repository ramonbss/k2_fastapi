from fastapi import APIRouter, Depends, HTTPException

from app.api.crud import get_user_by_id
from app.api.dependencies import validate_user_id
from app.api.services.user_service import fetch_user_purchases
from app.core.config import ROLE_USER

user_router = APIRouter()
TAG_USERS = "users"


@user_router.get("", tags=[TAG_USERS])
async def user_purchases(user_id: int = Depends(validate_user_id)):
    user = get_user_by_id(user_id)

    if not user.role == ROLE_USER:
        raise HTTPException(status_code=403, detail="You are not an user")

    return await fetch_user_purchases(user)
