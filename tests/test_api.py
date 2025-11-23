from httpx import AsyncClient


async def test_process_url_pair(ac: AsyncClient):
    result = await ac.post("/slug", json={"original_url": "https://example.com"})
    assert result.status_code == 200


async def test_redirect_on_original(ac: AsyncClient):
    slug_value = "slug"
    test_url = "https://example.com"

    # Add URL pair via POST /slug
    response = await ac.post("/slug", json={"original_url": test_url})
    assert response.status_code == 200
    assert response.json().get("slug") is not None

    # Use the slug from response or fixed one
    used_slug = response.json().get("slug", slug_value)

    # Check redirect for slug via GET /{slug}
    result = await ac.get(f"/{used_slug}")
    assert result.status_code in (302, 307)
    assert result.headers.get("location") == test_url
