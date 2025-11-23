from backend.main import app
from backend.src.dependencies import get_session
from backend.db.models import Base

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

import pytest


engine = create_async_engine(
    url="sqlite+aiosqlite:///./test.db",
    pool_size=20,
    max_overflow=30,
)
test_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_test_session() -> AsyncGenerator[AsyncSession, None]:
    async with test_session() as s:
        yield s


app.dependency_overrides[get_session] = get_test_session


@pytest.fixture()
async def setup_database(scope="session"):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
