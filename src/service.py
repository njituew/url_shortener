from src.short_url import generate_random_slug
from db.crud import add_pair


async def process_url(original_url: str):
    slug = await generate_random_slug()
    await add_pair(original_url, slug)
    return slug
