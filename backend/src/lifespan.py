from contextlib import asynccontextmanager
from fastapi import FastAPI
from db.database import engine
from db.models import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
