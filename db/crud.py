from db.database import session
from db.models import URL_Pair


async def add_pair(orig_url: str, slug: str):
    async with session() as s:
        new_data = URL_Pair(slug=slug, original_url=orig_url)
        s.add(new_data)
        await s.commit()
