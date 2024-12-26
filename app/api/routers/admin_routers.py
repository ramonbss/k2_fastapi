from fastapi import APIRouter, Depends, HTTPException

from app.api.crud import get_admin_by_id
from app.api.dependencies import validate_admin_id
from app.api.services.admin_service import fetch_admin_reports
from app.core.config import ROLE_ADMIN


admin_router = APIRouter()
TAG_ADMIN = "admin"


@admin_router.get("", tags=[TAG_ADMIN])
async def admin_reports(admin_id: int = Depends(validate_admin_id)):
    admin = get_admin_by_id(admin_id)

    if not admin.role == ROLE_ADMIN:
        raise HTTPException(status_code=403, detail="You are not an admin")

    return await fetch_admin_reports(admin)
