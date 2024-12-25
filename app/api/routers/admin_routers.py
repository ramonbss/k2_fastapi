from fastapi import APIRouter, Depends, HTTPException

from app.api.crud import get_admin_reports_from_db, get_admin_by_id, create_reports
from app.api.dependencies import validate_admin_id
from app.api.services.admin_service import (
    get_admin_reports_from_server,
    get_admin_access_token_from_server,
)


admin_router = APIRouter()
TAG_ADMIN = "admin"


@admin_router.get("", tags=[TAG_ADMIN])
async def admin_reports(admin_id: int = Depends(validate_admin_id)):
    admin = get_admin_by_id(admin_id)

    if not admin.role == "admin":
        raise HTTPException(status_code=403, detail="You are not an admin")

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

    return admin_reports
