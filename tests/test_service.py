from backend.src.service import make_urls_pair


async def test_generate_short_url(session):
    test_slug = await make_urls_pair("https://google.com", session)
    assert type(test_slug) is str
    assert len(test_slug) == 6
