import pytest
from httpx import AsyncClient


class TestSlugEndpoint:
    async def test_create_slug_success(self, ac: AsyncClient):
        response = await ac.post("/slug", json={"original_url": "https://example.com"})
        assert response.status_code == 200

    async def test_create_slug_response_shape(self, ac: AsyncClient):
        """Ответ должен содержать slug и original_url."""
        response = await ac.post("/slug", json={"original_url": "https://example.com"})
        body = response.json()
        assert "slug" in body
        assert "original_url" in body
        assert body["original_url"] == "https://example.com"

    async def test_create_slug_length(self, ac: AsyncClient):
        response = await ac.post("/slug", json={"original_url": "https://example.com"})
        slug = response.json()["slug"]
        assert len(slug) == 6

    async def test_invalid_url_returns_400(self, ac: AsyncClient):
        response = await ac.post("/slug", json={"original_url": "not-a-url"})
        assert response.status_code == 400

    async def test_missing_field_returns_422(self, ac: AsyncClient):
        """FastAPI должен вернуть 422 если поле original_url отсутствует."""
        response = await ac.post("/slug", json={})
        assert response.status_code == 422

    async def test_empty_url_returns_400(self, ac: AsyncClient):
        response = await ac.post("/slug", json={"original_url": ""})
        assert response.status_code == 400


class TestRedirectEndpoint:
    async def test_redirect_to_original(self, ac: AsyncClient):
        # Сначала создаём пару
        create = await ac.post("/slug", json={"original_url": "https://example.com"})
        slug = create.json()["slug"]

        # Проверяем редирект (follow_redirects=False чтобы увидеть 302)
        response = await ac.get(f"/{slug}", follow_redirects=False)
        assert response.status_code == 302
        assert response.headers["location"] == "https://example.com"

    async def test_nonexistent_slug_returns_404(self, ac: AsyncClient):
        response = await ac.get("/nonexistentslug123", follow_redirects=False)
        assert response.status_code == 404
