from app.api.services.service import get_access_token, get_user_informations
from app.core.config import ADMIN_USERNAME, ADMIN_PASSWORD, REMOTE_ADMIN_URL


async def get_admin_reports_from_server(token: str):
    """Access the remote /user endpoint using a valid JWT token."""
    data = await get_user_informations("admin", token, REMOTE_ADMIN_URL)
    return data


async def get_admin_access_token_from_server():
    username = ADMIN_USERNAME
    password = ADMIN_PASSWORD
    token = await get_access_token(username, password, "admin")
    return token
