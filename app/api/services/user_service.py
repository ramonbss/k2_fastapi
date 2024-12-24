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
