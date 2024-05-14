from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from db.db import create_db_and_tables
from api.routers import main_api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan, include_in_schema=True)
app.include_router(main_api_router)


@app.get('/', response_class=RedirectResponse)
async def redirect_to_docs():
    return '/docs'
