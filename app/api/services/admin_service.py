from fastapi import HTTPException
from app.api.crud import (
    create_or_update_user,
    create_reports,
    get_admin_reports_from_db,
    get_user_by_username,
)
from app.api.database import Admin
from app.api.services.service import get_access_token, get_user_informations
from app.core.config import ADMIN_USERNAME, ADMIN_PASSWORD, REMOTE_ADMIN_URL


async def initiate_admin_database():
    user = get_user_by_username(ADMIN_USERNAME, Admin)
    if user:
        return
    admin_token = await get_admin_access_token_from_server()

    create_or_update_user(username=ADMIN_USERNAME, role=ROLE_ADMIN, token=admin_token)


async def get_admin_reports_from_server(token: str):
    """Access the remote /user endpoint using a valid JWT token."""
    data = await get_user_informations(ROLE_ADMIN, token, REMOTE_ADMIN_URL)
    return data


async def get_admin_access_token_from_server():
    username = ADMIN_USERNAME
    password = ADMIN_PASSWORD
    token = await get_access_token(username, password, ROLE_ADMIN)
    return token


async def fetch_admin_reports(admin: Admin):
    admin_access_token = admin.token
    if not admin_access_token:
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
