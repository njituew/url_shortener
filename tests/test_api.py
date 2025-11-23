from httpx import AsyncClient


async def test_generate_slug(ac: AsyncClient):
    result = await ac.post("/slug", json={"original_url": "https://example.com"})
    assert result.status_code == 200
