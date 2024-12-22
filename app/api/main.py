from fastapi import FastAPI, Depends, HTTPException
import httpx
from .models import UserCredentials
from ..core.config import FAKE_API_TOKEN_ENDPOINT

app = FastAPI()


@app.post("/token")
async def authenticate(credentials: UserCredentials):
    async with httpx.AsyncClient(verify=False) as client:
        auth_data = {"username": credentials.username, "password": credentials.password}
        response = await client.post(FAKE_API_TOKEN_ENDPOINT, params=auth_data)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Invalid credentials")
        return response.json()
