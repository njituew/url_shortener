import string
import pytest
from src.service import make_urls_pair, get_url_by_slug
from src.exception import NoOriginalUrlFoundError, InvalidURL_Error


VALID_SLUG_CHARS = set(string.ascii_letters + string.digits)


class TestMakeUrlsPair:
    async def test_returns_string(self, session):
        slug = await make_urls_pair("https://google.com", session)
        assert isinstance(slug, str)

    async def test_slug_length(self, session):
        slug = await make_urls_pair("https://google.com", session)
        assert len(slug) == 6

    async def test_slug_charset(self, session):
        """Slug должен состоять только из букв и цифр."""
        slug = await make_urls_pair("https://google.com", session)
        assert set(slug).issubset(VALID_SLUG_CHARS)

    async def test_different_urls_get_different_slugs(self, session):
        slug1 = await make_urls_pair("https://google.com", session)
        slug2 = await make_urls_pair("https://github.com", session)
        assert slug1 != slug2

    async def test_invalid_url_raises(self, session):
        with pytest.raises(InvalidURL_Error):
            await make_urls_pair("not-a-url", session)

    async def test_invalid_url_no_scheme_raises(self, session):
        with pytest.raises(InvalidURL_Error):
            await make_urls_pair("example.com", session)

    async def test_ftp_scheme_raises(self, session):
        with pytest.raises(InvalidURL_Error):
            await make_urls_pair("ftp://example.com", session)

    async def test_empty_url_raises(self, session):
        with pytest.raises(InvalidURL_Error):
            await make_urls_pair("", session)


class TestGetUrlBySlug:
    async def test_returns_correct_url(self, session):
        original_url = "https://example.com"
        slug = await make_urls_pair(original_url, session)
        result = await get_url_by_slug(slug, session)
        assert result == original_url

    async def test_nonexistent_slug_raises(self, session):
        with pytest.raises(NoOriginalUrlFoundError):
            await get_url_by_slug("nonexistent", session)

    async def test_roundtrip(self, session):
        """Сохранённый URL должен точно совпадать с извлечённым."""
        url = "https://example.com/path?foo=bar&baz=qux"
        slug = await make_urls_pair(url, session)
        assert await get_url_by_slug(slug, session) == url
