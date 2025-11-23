from db.database import session
from db.models import URL_Pair

from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError

from src.exception import SlugAlreadyExistsError


async def add_pair(orig_url: str, slug: str):
    async with session() as s:
        new_data = URL_Pair(slug=slug, original_url=orig_url)
        s.add(new_data)
        try:
            await s.commit()
        except IntegrityError:
            raise SlugAlreadyExistsError


async def get_original_url(slug: str) -> str | None:
    async with session() as s:
        query = select(URL_Pair).where(URL_Pair.slug == slug)
        result = await s.execute(query)
        res: URL_Pair | None = result.scalar_one_or_none()
        return res.original_url if res and res.original_url else None


async def clear_all_pairs():
    async with session() as s:
        stmt = delete(URL_Pair)
        await s.execute(stmt)
        await s.commit()
