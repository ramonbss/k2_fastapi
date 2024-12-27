from fastapi import FastAPI, Depends, HTTPException
import httpx

from app.api.services.admin_service import initiate_admin_database
from app.api.services.user_service import initiate_user_database

from .models import UserCredentials
from ..core.config import REMOTE_TOKEN_URL
from .dependencies import (
    validate_token,
)
from sqlalchemy.orm import Session

from .crud import (
    create_or_update_user,
    get_database,
)
from app.api.routers import user_routers, admin_routers

fast_app = FastAPI()

fast_app.include_router(
    user_routers.user_router, prefix="/purchase", tags=[user_routers.TAG_USERS]
)

fast_app.include_router(
    admin_routers.admin_router, prefix="/report", tags=[admin_routers.TAG_ADMIN]
)


@fast_app.on_event("startup")
async def start_up():
    await initiate_user_database()
    await initiate_admin_database()
