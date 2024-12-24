from app.api.services.service import get_user_informations
from app.core.config import REMOTE_ADMIN_URL


async def get_admin_reports_from_server(token: str):
    """Access the remote /user endpoint using a valid JWT token."""
    data = await get_user_informations("admin", token, REMOTE_ADMIN_URL)
    return data
