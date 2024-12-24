from fastapi import HTTPException
import httpx
from app.api.crud import reset_access_token
from app.api.database import Admin, User
from app.api.dependencies import check_role


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
