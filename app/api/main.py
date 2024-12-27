from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.api.services.admin_service import initiate_admin_database
from app.api.services.user_service import initiate_user_database
from starlette.exceptions import HTTPException

fast_app = FastAPI()


@fast_app.exception_handler(HTTPException)
async def custom_http_exception_handler(request, exc):
    if exc.status_code == 404:
        return JSONResponse(
            {
                "detail": "The requested endpoit was not found. Use '/purchase' or '/report'"
            },
            status_code=404,
        )
    return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)


from app.api.routers import user_routers, admin_routers

fast_app.include_router(
    user_routers.user_router, prefix="/purchase", tags=[user_routers.TAG_USERS]
)

fast_app.include_router(
    admin_routers.admin_router, prefix="/report", tags=[admin_routers.TAG_ADMIN]
)


@fast_app.on_event("startup")
async def start_up():
    await initiate_user_database()
    await initiate_admin_database()
