from httpx import AsyncClient
from datetime import date

base_url = "/products"
product_id: int
guarantee_end_date: date


async def test_add_product(ac: AsyncClient):
    response = await ac.post(
        base_url,
        json={
            "name": "Xiaomi Notebook",
            "model": "Air 13.3",
            "price": 49899.30,
            "is_purchased": True,
            "buy_date": "2024-10-12",
            "receipt": "http://example.com/prodict1",
            "shop": "Amazon",
            "priority": 1,
        },
    )

    assert response.status_code == 200
    response = response.json()
    assert response["ok"] == True
    assert "product_id" in response["content"].keys()
    assert "guarantee" in response["content"]["auto_generated_fields"].keys()
    assert "guarantee_end_date" in response["content"]["auto_generated_fields"].keys()

    global product_id, guarantee_end_date
    product_id = response["content"]["product_id"]
    guarantee_end_date = response["content"]["auto_generated_fields"][
        "guarantee_end_date"
    ]


async def test_get_product(ac: AsyncClient):
    chunk_size = 25

    response = await ac.get(
        base_url,
        params={"by": chunk_size, "chunk": 0, "field": "id", "desc": False},
    )

    assert response.status_code == 200
    response = response.json()
    assert response["ok"] == True
    assert len(response["content"]) <= response["total_count"]
    assert len(response["content"]) <= chunk_size


async def test_update_product(ac: AsyncClient):
    response = await ac.patch(
        base_url,
        json={"id": product_id, "guarantee": 2, "model": "Air 14.4"},
    )

    assert response.status_code == 200
    response = response.json()
    assert response["ok"] == True
    assert response["content"]["name"] == "Xiaomi Notebook"
    assert response["content"]["guarantee"] == 2
    assert guarantee_end_date != response["content"]["guarantee_end_date"]


async def test_delete_product(ac: AsyncClient):
    response = await ac.delete(
        base_url,
        params={"product_id": product_id},
    )

    assert response.status_code == 200
    response = response.json()
    assert response["ok"] == True
