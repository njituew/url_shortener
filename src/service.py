from db.crud import add_pair, get_original_url
from src.short_url import generate_random_slug
from src.exception import (
    NoOriginalUrlFoundError,
    SlugAlreadyExistsError,
    InvalidURL_Error,
)
from src.url_validator import is_valid_url


async def make_urls_pair(original_url: str) -> str:
    async def __generate_slug_and_add_to_db(original_url: str) -> str:
        slug = await generate_random_slug()
        await add_pair(original_url, slug)
        return slug

    if is_valid_url(original_url) is False:
        raise InvalidURL_Error

    for attempt in range(5):
        try:
            slug = await __generate_slug_and_add_to_db(original_url)
            return slug
        except SlugAlreadyExistsError as ex:
            if attempt == 4:
                raise SlugAlreadyExistsError from ex
        except Exception as ex:
            if attempt == 4:
                raise Exception from ex
            else:
                continue


async def get_url_by_slug(slug: str) -> str:
    original_url = await get_original_url(slug)
    if not original_url:
        raise NoOriginalUrlFoundError()
    return original_url
