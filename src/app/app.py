from contextlib import asynccontextmanager
from fastapi import FastAPI

from db.db import create_db_and_tables
from api.routers import main_api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(main_api_router)



