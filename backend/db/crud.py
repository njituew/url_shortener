# from db.database import session
from db.models import URL_Pair

from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.exception import SlugAlreadyExistsError


async def add_pair(orig_url: str, slug: str, session: AsyncSession):
    # async with session() as s:
    new_data = URL_Pair(slug=slug, original_url=orig_url)
    session.add(new_data)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise SlugAlreadyExistsError


async def get_original_url(slug: str, session: AsyncSession) -> str | None:
    # async with session() as s:
    query = select(URL_Pair).where(URL_Pair.slug == slug)
    result = await session.execute(query)
    res: URL_Pair | None = result.scalar_one_or_none()
    return res.original_url if res and res.original_url else None


async def clear_all_pairs(session: AsyncSession):
    stmt = delete(URL_Pair)
    await session.execute(stmt)
    await session.commit()
