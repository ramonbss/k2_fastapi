from fastapi import FastAPI, Depends, HTTPException
import httpx
from .models import UserCredentials
from ..core.config import REMOTE_TOKEN_URL, REMOTE_USER_URL, REMOTE_ADMIN_URL
from .dependencies import validate_token

app = FastAPI()


@app.post("/token")
async def authenticate(credentials: UserCredentials):
    async with httpx.AsyncClient(verify=False) as client:
        auth_data = {"username": credentials.username, "password": credentials.password}
        response = await client.post(REMOTE_TOKEN_URL, params=auth_data)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Invalid credentials")
        return response.json()


@app.get("/user")
async def local_user(token: str = Depends(validate_token)):
    """Access the remote /user endpoint using a valid JWT token."""
    async with httpx.AsyncClient(verify=False) as client:
        headers = {"Authorization": token}
        response = await client.get(REMOTE_USER_URL, headers=headers)
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code, detail=response.json()
            )
        return response.json()


@app.get("/admin")
async def local_admin(token: str = Depends(validate_token)):
    """Access the remote /user endpoint using a valid JWT token."""
    async with httpx.AsyncClient(verify=False) as client:
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.get(REMOTE_ADMIN_URL, headers=headers)
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code, detail=response.json()
            )
        return response.json()
