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
        create = await ac.post("/slug", json={"original_url": "https://example.com"})
        slug = create.json()["slug"]

        response = await ac.get(f"/{slug}", follow_redirects=False)
        assert response.status_code == 302
        assert response.headers["location"] == "https://example.com"

    async def test_nonexistent_slug_returns_404(self, ac: AsyncClient):
        response = await ac.get("/nonexistentslug123", follow_redirects=False)
        assert response.status_code == 404


class TestGetSlugsEndpoint:
    async def test_returns_list(self, ac: AsyncClient):
        response = await ac.get("/slugs")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    async def test_created_slug_appears_in_list(self, ac: AsyncClient):
        """Созданный slug должен быть виден в GET /slugs."""
        create = await ac.post("/slug", json={"original_url": "https://list-check.com"})
        slug = create.json()["slug"]

        response = await ac.get("/slugs")
        slugs = [item["slug"] for item in response.json()]
        assert slug in slugs

    async def test_list_item_shape(self, ac: AsyncClient):
        """Каждый элемент списка должен содержать slug и original_url."""
        await ac.post("/slug", json={"original_url": "https://shape-check.com"})

        response = await ac.get("/slugs")
        items = response.json()
        assert len(items) > 0
        for item in items:
            assert "slug" in item
            assert "original_url" in item


class TestDeleteSlugEndpoint:
    async def test_delete_existing_slug_returns_200(self, ac: AsyncClient):
        create = await ac.post("/slug", json={"original_url": "https://to-delete.com"})
        slug = create.json()["slug"]

        response = await ac.delete(f"/slugs/{slug}")
        assert response.status_code == 200

    async def test_deleted_slug_no_longer_redirects(self, ac: AsyncClient):
        """После удаления GET /{slug} должен возвращать 404."""
        create = await ac.post("/slug", json={"original_url": "https://gone.com"})
        slug = create.json()["slug"]

        await ac.delete(f"/slugs/{slug}")

        response = await ac.get(f"/{slug}", follow_redirects=False)
        assert response.status_code == 404

    async def test_deleted_slug_absent_from_list(self, ac: AsyncClient):
        """После удаления slug не должен появляться в GET /slugs."""
        create = await ac.post("/slug", json={"original_url": "https://absent.com"})
        slug = create.json()["slug"]

        await ac.delete(f"/slugs/{slug}")

        response = await ac.get("/slugs")
        slugs = [item["slug"] for item in response.json()]
        assert slug not in slugs

    async def test_delete_nonexistent_slug_returns_404(self, ac: AsyncClient):
        response = await ac.delete("/slugs/nonexistent")
        assert response.status_code == 404

    async def test_double_delete_returns_404(self, ac: AsyncClient):
        """Повторное удаление того же slug должно вернуть 404."""
        create = await ac.post("/slug", json={"original_url": "https://double-delete.com"})
        slug = create.json()["slug"]

        await ac.delete(f"/slugs/{slug}")
        response = await ac.delete(f"/slugs/{slug}")
        assert response.status_code == 404


class TestDeleteAllSlugsEndpoint:
    async def test_delete_all_returns_200(self, ac: AsyncClient):
        response = await ac.delete("/slugs")
        assert response.status_code == 200

    async def test_delete_all_clears_list(self, ac: AsyncClient):
        """После DELETE /slugs список должен быть пустым."""
        await ac.post("/slug", json={"original_url": "https://clear-a.com"})
        await ac.post("/slug", json={"original_url": "https://clear-b.com"})

        await ac.delete("/slugs")

        response = await ac.get("/slugs")
        assert response.json() == []

    async def test_delete_all_idempotent(self, ac: AsyncClient):
        """Повторный DELETE /slugs на пустой таблице тоже должен вернуть 200."""
        await ac.delete("/slugs")
        response = await ac.delete("/slugs")
        assert response.status_code == 200
