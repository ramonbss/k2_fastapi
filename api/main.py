from fastapi import FastAPI, Depends, HTTPException
import httpx
from .models import UserCredentials

app = FastAPI()
FAKE_API_URL = "https://api-onecloud.multicloud.tivit.com/fake/"
FAKE_API_TOKEN_ENDPOINT = FAKE_API_URL + "token"


@app.post("/token")
async def authenticate(credentials: UserCredentials):
    async with httpx.AsyncClient(verify=False) as client:
        auth_data = {"username": credentials.username, "password": credentials.password}
        response = await client.post(FAKE_API_TOKEN_ENDPOINT, params=auth_data)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Invalid credentials")
        return response.json()
