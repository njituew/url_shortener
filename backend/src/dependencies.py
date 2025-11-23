from db.database import session
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with session() as s:
        yield s
