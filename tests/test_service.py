import pytest
from src.service import make_urls_pair, get_url_by_slug
from src.exception import NoOriginalUrlFoundError


async def test_generate_short_url(session):
    test_slug = await make_urls_pair("https://google.com", session)
    assert type(test_slug) is str
    assert len(test_slug) == 6


async def test_get_url_by_slug(session):
    original_url = "https://example.com"
    slug = await make_urls_pair(original_url, session)

    result = await get_url_by_slug(slug, session)
    assert result == original_url

    try:
        await get_url_by_slug("nonexistentslug", session)
    except Exception as exc:
        print(f"Caught exception type: {type(exc)}")
        print(f"Caught exception: {exc}")
        assert isinstance(
            exc, NoOriginalUrlFoundError
        ), f"Exception type mismatch: {type(exc)}"
    else:
        pytest.fail("NoOriginalUrlFoundError was not raised")
