from db.crud import add_pair, get_original_url
from src.short_url import generate_random_slug
from src.exception import (
    NoOriginalUrlFoundError,
    SlugAlreadyExistsError,
    InvalidURL_Error,
)
from src.url_validator import is_valid_url
from sqlalchemy.ext.asyncio import AsyncSession


async def make_urls_pair(original_url: str, session: AsyncSession) -> str:
    async def __generate_slug_and_save_pair(
        original_url: str, session: AsyncSession
    ) -> str:
        slug = await generate_random_slug()
        await add_pair(original_url, slug, session)
        return slug

    if not is_valid_url(original_url):
        raise InvalidURL_Error

    for attempt in range(5):
        try:
            slug = await __generate_slug_and_save_pair(original_url, session)
            return slug
        except SlugAlreadyExistsError as ex:
            if attempt == 4:
                raise SlugAlreadyExistsError from ex
        except Exception as ex:
            if attempt == 4:
                raise Exception from ex
            else:
                continue


async def get_url_by_slug(slug: str, session: AsyncSession) -> str:
    original_url = await get_original_url(slug, session)
    if not original_url:
        raise NoOriginalUrlFoundError()
    return original_url
