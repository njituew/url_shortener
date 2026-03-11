from db.models import URL_Pair

from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.exception import SlugAlreadyExistsError


async def add_pair(orig_url: str, slug: str, session: AsyncSession):
    new_data = URL_Pair(slug=slug, original_url=orig_url)
    session.add(new_data)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise SlugAlreadyExistsError


async def get_original_url(slug: str, session: AsyncSession) -> str | None:
    query = select(URL_Pair).where(URL_Pair.slug == slug)
    result = await session.execute(query)
    res: URL_Pair | None = result.scalar_one_or_none()
    return res.original_url if res and res.original_url else None


async def get_all_pairs(session: AsyncSession) -> list[URL_Pair]:
    query = select(URL_Pair).order_by(URL_Pair.slug)
    result = await session.execute(query)
    return list(result.scalars().all())


async def delete_pair_by_slug(slug: str, session: AsyncSession) -> bool:
    """Deletes a pair by slug

    Returns:
        bool: True if the record was found and deleted
    """
    query = delete(URL_Pair).where(URL_Pair.slug == slug).returning(URL_Pair.slug)
    result = await session.execute(query)
    await session.commit()
    return result.fetchone() is not None


async def delete_all_pairs(session: AsyncSession):
    stmt = delete(URL_Pair)
    await session.execute(stmt)
    await session.commit()
