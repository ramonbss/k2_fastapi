from fastapi import HTTPException
import httpx
from app.api.crud import reset_access_token
from app.api.dependencies import check_role
from app.api.services.service import get_user_informations
from app.core.config import REMOTE_USER_URL


async def get_user_purchases_from_server(token: str):
    """Access the remote /user endpoint using a valid JWT token."""
    data = await get_user_informations("user", token, REMOTE_USER_URL)
    return data