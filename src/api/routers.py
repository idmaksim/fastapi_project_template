from fastapi import APIRouter
from . import users

main_api_router = APIRouter(
    prefix='/api'
)

routers = [
    users.router
]

[main_api_router.include_router(router) for router in routers]