from contextlib import asynccontextmanager
from typing import Any
from fastapi import APIRouter, FastAPI

from .database import create_db_and_tables

from .routers import (
    user
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield



def init_app(app: FastAPI) ->  FastAPI:
    api_router = APIRouter(
        prefix='/api'
    )        
    api_router.include_router(user.router)
    app.include_router(api_router)
    
    return app


app = init_app(FastAPI(lifespan=lifespan))






