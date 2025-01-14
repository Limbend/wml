from httpx import AsyncClient
from datetime import date
import pytest


@pytest.fixture(scope="class")
async def product_data():
    data = {"product_id": None, "guarantee_end_date": None}
    yield data


class TestProductApi:
    base_url = "/products"

    @pytest.mark.dependency(name="add", scope="session")
    async def test_add_product(self, ac: AsyncClient, product_data):
        response = await ac.post(
            self.base_url,
            json={
                "name": "Xiaomi Notebook",
                "model": "Air 13.3",
                "price": 49899.30,
                "is_purchased": True,
                "buy_date": "2024-10-12",
                "guarantee": 12,
                "product_link": "https://www.mi.com",
                "priority": 1,
            },
        )

        assert response.status_code == 200
        response = response.json()
        assert response["ok"] == True
        assert "product_id" in response["content"].keys()
        assert (
            "guarantee_end_date" in response["content"]["auto_generated_fields"].keys()
        )

        product_data["product_id"] = response["content"]["product_id"]
        product_data["guarantee_end_date"] = response["content"][
            "auto_generated_fields"
        ]["guarantee_end_date"]

    @pytest.mark.dependency(depends=["add"], name="get", scope="session")
    async def test_get_product(self, ac: AsyncClient):
        chunk_size = 25

        response = await ac.get(
            self.base_url,
            params={"by": chunk_size, "chunk": 0, "field": "id", "desc": False},
        )

        assert response.status_code == 200
        response = response.json()
        assert response["ok"] == True
        assert len(response["content"]) <= response["total_count"]
        assert len(response["content"]) <= chunk_size

    @pytest.mark.dependency(depends=["add"], name="update", scope="session")
    async def test_update_product(self, ac: AsyncClient, product_data):
        response = await ac.patch(
            self.base_url,
            json={
                "id": product_data["product_id"],
                "guarantee": 2,
                "model": "Air 14.4",
            },
        )

        assert response.status_code == 200
        response = response.json()
        assert response["ok"] == True
        assert response["content"]["name"] == "Xiaomi Notebook"
        assert response["content"]["guarantee"] == 2
        assert (
            product_data["guarantee_end_date"]
            != response["content"]["guarantee_end_date"]
        )

    @pytest.mark.dependency(depends=["add", "get", "update"], scope="session")
    async def test_delete_product(self, ac: AsyncClient, product_data):
        response = await ac.delete(
            self.base_url,
            params={"product_id": product_data["product_id"]},
        )

        assert response.status_code == 200
        response = response.json()
        assert response["ok"] == True
