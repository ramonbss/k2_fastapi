from fastapi import HTTPException
import httpx
from app.api.crud import create_or_update_user, reset_access_token
from app.api.database import Admin, User
from app.api.dependencies import check_role
from app.core.config import REMOTE_TOKEN_URL


async def get_user_informations(role: str, token: str, ENDPOINT_URL):
    await check_role(role, token.split(" ")[1])
    async with httpx.AsyncClient(verify=False) as client:
        headers = {"Authorization": token}
        response = await client.get(ENDPOINT_URL, headers=headers)
        instance = User if role == "user" else Admin
        if response.status_code == 401:
            reset_access_token(token.split(" ")[1], instance)
            raise HTTPException(
                status_code=401, detail="Error while authenticating, try again"
            )
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code, detail=response.json()
            )
        return response.json()


async def get_access_token(username: str, password: str, role):
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.post(
            REMOTE_TOKEN_URL,
            params={"username": username, "role": role, "password": password},
        )
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code, detail=response.json()
            )
        access_token = response.json()["access_token"]
        create_or_update_user(username=username, role=role, token=access_token)
        return access_token
