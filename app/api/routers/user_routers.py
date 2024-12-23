from fastapi import APIRouter, Depends, HTTPException

from app.api.crud import create_purchases, get_user_by_id, get_user_purchases_from_db
from app.api.dependencies import validate_user_id
from app.api.services.user_service import get_user_purchases_from_server

user_router = APIRouter()
TAG_USERS = "users"


@user_router.get("", tags=[TAG_USERS])
async def user_purchases(user_id: int = Depends(validate_user_id)):
    user = get_user_by_id(user_id)

    if not user.role == "user":
        raise HTTPException(status_code=403, detail="You are not a user")

    users_purchases = get_user_purchases_from_db(user.id)

    if not users_purchases:
        get_purchases_result = await get_user_purchases_from_server(
            f"Bearer {user.token}"
        )
        if not get_purchases_result or "data" not in get_purchases_result:
            raise HTTPException(status_code=403, detail="Error while gathering data")

        create_purchases(user.token, get_purchases_result["data"])
        users_purchases = get_user_purchases_from_db(user.id)

    response = ""

    for p in users_purchases:
        response += p.to_string() + "\n"

    return response
