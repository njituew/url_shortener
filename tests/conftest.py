import pytest

from httpx import ASGITransport, AsyncClient

from src.dependencies import get_session  # единый путь через pythonpath=backend
from main import app
from db.models import Base

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

from typing import AsyncGenerator


engine = create_async_engine(url="sqlite+aiosqlite:///./test.db")
test_session = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_test_session() -> AsyncGenerator[AsyncSession, None]:
    async with test_session() as s:
        yield s


app.dependency_overrides[get_session] = get_test_session


@pytest.fixture(scope="session", autouse=True)
async def setup_db():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="function")
async def session():
    async with test_session() as s:
        yield s


@pytest.fixture(scope="session")
async def ac(setup_db) -> AsyncGenerator[AsyncClient, None]:  # явная зависимость от setup_db
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
