from fastapi import FastAPI, Depends, HTTPException
import httpx
from .models import UserCredentials
from ..core.config import REMOTE_TOKEN_URL, REMOTE_USER_URL, REMOTE_ADMIN_URL
from .dependencies import (
    get_database,
    validate_token,
    check_if_user_role,
    check_if_admin_role,
    check_role,
)
from sqlalchemy.orm import Session

from .crud import create_or_update_user, reset_access_token

app = FastAPI()


@app.post("/token")
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


@app.get("/user")
async def local_user(token: str = Depends(validate_token)):
    """Access the remote /user endpoint using a valid JWT token."""
    data = await get_user_informations("user", token, REMOTE_USER_URL)
    return data


@app.get("/admin")
async def local_admin(token: str = Depends(validate_token)):
    """Access the remote /user endpoint using a valid JWT token."""
    data = await get_user_informations("admin", token, REMOTE_ADMIN_URL)
    return data


async def get_user_informations(role: str, token: str, ENDPOINT_URL):
    await check_role(role, token.split(" ")[1])
    async with httpx.AsyncClient(verify=False) as client:
        headers = {"Authorization": token}
        response = await client.get(ENDPOINT_URL, headers=headers)
        if response.status_code == 401:
            reset_access_token(token.split(" ")[1])
            raise HTTPException(status_code=401, detail="Token expired")
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code, detail=response.json()
            )
        return response.json()
