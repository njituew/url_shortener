from db.crud import add_pair, get_original_url
from src.short_url import generate_random_slug
from src.exception import (
    NoOriginalUrlFoundError,
    SlugAlreadyExistsError,
    InvalidURL_Error,
)
from src.url_validator import is_valid_url
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError


async def make_urls_pair(original_url: str, session: AsyncSession) -> str:
    if not is_valid_url(original_url):
        raise InvalidURL_Error

    for attempt in range(5):
        slug = await generate_random_slug()

        try:
            await add_pair(original_url, slug, session)
            return slug

        except SlugAlreadyExistsError:
            if attempt == 4:
                raise

        except IntegrityError:
            raise

        except Exception:
            raise

    raise SlugAlreadyExistsError


async def get_url_by_slug(slug: str, session: AsyncSession) -> str:
    original_url = await get_original_url(slug, session)
    if not original_url:
        raise NoOriginalUrlFoundError
    return original_url
