from fastapi import FastAPI, Depends, HTTPException
import httpx

from app.api.services.service import get_user_informations
from .models import UserCredentials
from ..core.config import REMOTE_TOKEN_URL, REMOTE_ADMIN_URL
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
    user_routers.user_router, prefix="/user", tags=[user_routers.TAG_USERS]
)

fast_app.include_router(
    admin_routers.admin_router, prefix="/admin", tags=[admin_routers.TAG_ADMIN]
)


@fast_app.post("/token")
async def authenticate(
    credentials: UserCredentials, db: Session = Depends(get_database)
):
    async with httpx.AsyncClient(verify=False) as client:
        auth_data = {"username": credentials.username, "password": credentials.password}
        response = await client.post(REMOTE_TOKEN_URL, params=auth_data)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Invalid credentials")
        token = response.json()["access_token"]
        create_or_update_user(
            db=db, username=credentials.username, role=credentials.role, token=token
        )
        return response.json()
