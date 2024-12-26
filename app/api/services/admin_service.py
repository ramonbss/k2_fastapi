from fastapi import HTTPException
from app.api.crud import create_reports, get_admin_reports_from_db
from app.api.database import Admin
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


async def fetch_admin_reports(admin: Admin):
    if not admin.token:
        admin_access_token = await get_admin_access_token_from_server()

    admins_reports = get_admin_reports_from_db(admin.id)

    if not admins_reports:
        get_reports_result = await get_admin_reports_from_server(
            f"Bearer {admin_access_token}"
        )
        if not get_reports_result or "data" not in get_reports_result:
            raise HTTPException(status_code=403, detail="Error while gathering data")

        create_reports(admin.token, get_reports_result["data"])
        admins_reports = get_admin_reports_from_db(admin.id)

    admin_reports = []

    for p in admins_reports:
        admin_reports.append(p.to_dict())

    return {"reports": admin_reports}
