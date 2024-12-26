from fastapi import HTTPException
from app.api.crud import (
    create_or_update_user,
    create_purchases,
    get_user_purchases_from_db,
    get_user_by_username,
)
from app.api.database import User
from app.api.services.service import get_user_informations
from app.core.config import REMOTE_USER_URL, ROLE_USER, USER_USERNAME, USER_PASSWORD
from app.api.services.service import get_access_token


async def initiate_user_database():
    user = get_user_by_username(USER_USERNAME, User)
    if user:
        return
    user_token = await get_user_access_token_from_server()

    create_or_update_user(username=USER_USERNAME, role=ROLE_USER, token=user_token)


async def get_user_purchases_from_server(token: str):
    """Access the remote /user endpoint using a valid JWT token."""
    data = await get_user_informations(ROLE_USER, token, REMOTE_USER_URL)
    return data


async def get_user_access_token_from_server():
    username = USER_USERNAME
    password = USER_PASSWORD
    token = await get_access_token(username, password, ROLE_USER)
    return token


async def fetch_user_purchases(user: User):
    user_access_token = user.token
    if not user_access_token:
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
