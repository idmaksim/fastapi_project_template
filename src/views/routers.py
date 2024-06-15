from fastapi import APIRouter
from views.user import router as user_router


main_api_router = APIRouter(
    prefix='/api'
)

routers = [
    user_router
]

[main_api_router.include_router(router) for router in routers]