from typing import Annotated
from fastapi import APIRouter, Body, Depends

from repository import ProductRepo
from schemas import (
    SBaseResponse,
    SProductEdit,
    SPagination,
    SProductAdd,
    SResponseAdd,
    SResponseGet,
    SResponseUpdate,
    SSort,
)

router = APIRouter(prefix="/products", tags=["products"])


@router.get("")
async def get_products(
    padding: Annotated[SPagination, Depends()], sorting: Annotated[SSort, Depends()]
) -> SResponseGet:
    products = await ProductRepo.get_list(padding, sorting)
    return products


@router.post("")
async def add_products(product: Annotated[SProductAdd, Body()]) -> SResponseAdd:
    resolve = await ProductRepo.add_one(product)
    return resolve


@router.delete("")
async def del_products(product_id: int) -> SBaseResponse:
    resolve = await ProductRepo.hide_one(product_id=product_id)
    return resolve


@router.patch("")
async def edit_one(
    edit_product: Annotated[
        SProductEdit,
        Body(
            openapi_examples={
                "one": {
                    "summary": "One field",
                    "description": "Update a single field. You can change any `SProductEdit` field. Regardless of the number of fields to be modified, `product.id` must be passed!",
                    "value": {"id": 1, "price": 50.01},
                },
                "multiple": {
                    "summary": "Multiple fields",
                    "description": "Update multiple fields.",
                    "value": {
                        "id": 1,
                        "price": 50.01,
                        "model": "super pro max extra ++",
                        "buy_date": "2024-09-29",
                    },
                },
                "all": {
                    "summary": "All fields",
                    "description": "Completely rewrite the product, replacing all fields.",
                    "value": {
                        "id": 1,
                        "name": "Gamer's spoon",
                        "price": 50.01,
                        "model": "super pro max extra ++",
                        "is_purchased": False,
                        "buy_date": "2024-09-29",
                        "guarantee": 2,
                        "receipt": "string",
                        "shop": "https://amazon.com",
                        "priority": 0,
                    },
                },
            }
        ),
    ]
) -> SResponseUpdate:
    resolve = await ProductRepo.edit_one(edit_product)
    return resolve
