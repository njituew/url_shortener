from db.crud import add_pair, get_original_url
from src.short_url import generate_random_slug
from src.exception import NoOriginalUrlFoundError


async def process_url(original_url: str) -> str:
    slug = await generate_random_slug()
    await add_pair(original_url, slug)
    return slug


async def get_url_by_slug(slug: str) -> str:
    original_url = await get_original_url(slug)
    if not original_url:
        raise NoOriginalUrlFoundError()
    return original_url