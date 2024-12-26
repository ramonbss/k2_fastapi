from fastapi import HTTPException
from app.api.crud import create_purchases, get_user_purchases_from_db
from app.api.database import User
from app.api.services.service import get_user_informations
from app.core.config import REMOTE_USER_URL, USER_USERNAME, USER_PASSWORD
from app.api.services.service import get_access_token


async def get_user_purchases_from_server(token: str):
    """Access the remote /user endpoint using a valid JWT token."""
    data = await get_user_informations("user", token, REMOTE_USER_URL)
    return data


async def get_user_access_token_from_server():
    username = USER_USERNAME
    password = USER_PASSWORD
    token = await get_access_token(username, password, "user")
    return token


async def fetch_user_purchases(user: User):
    if not user.token:
        user_access_token = await get_user_access_token_from_server()

    users_purchases = get_user_purchases_from_db(user.id)

    if not users_purchases:
        get_purchases_result = await get_user_purchases_from_server(
            f"Bearer {user_access_token}"
        )
        if not get_purchases_result or "data" not in get_purchases_result:
            raise HTTPException(status_code=403, detail="Error while gathering data")

        create_purchases(user.token, get_purchases_result["data"])
        users_purchases = get_user_purchases_from_db(user.id)

    user_purchases = []

    for p in users_purchases:
        user_purchases.append(p.to_dict())

    return {"purchases": user_purchases}
