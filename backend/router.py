from typing import Annotated
from fastapi import APIRouter, Body, Depends

from repository import ProductRepo
from schemas import SPagination, SProductAdd, SProductList, SResponseAdd, SResponseUpdate

router = APIRouter(
    prefix='/products',
    tags=['products']
)


@router.get('')
async def get_products(padding: Annotated[SPagination, Depends()]) -> SProductList:
    products = await ProductRepo.get_list(padding)
    return products


@router.post('')
async def add_products(product: Annotated[SProductAdd, Body()]) -> SResponseAdd:
    resolve = await ProductRepo.add_one(product)
    return resolve


@router.patch('')
async def update_one(
        id: int,
        data: Annotated[
            dict,
            Body(
                openapi_examples={
                    "one": {
                        "summary": "One parameters",
                        "description": "Update a single parameter. You can change any `product` parameter that is available during the creation of a new.",
                        "value": {'price': 50.01},
                    },
                    "multiple": {
                        "summary": "Multiple parameters",
                        "description": "Update multiple parameters. You can change several parameters at once. But if you need to update the whole object, use the `put` method.",
                        "value": {'price': 50.01, 'model': 'super pro max extra ++', 'buy_date': '2024-09-26'},
                    }
                },
            ),
        ]) -> SResponseUpdate:
    resolve = await ProductRepo.update_one(id, data)
    return resolve


@router.put('')
async def edit_products(id: int, product: Annotated[SProductAdd, Body()]) -> SResponseUpdate:
    resolve = await ProductRepo.replase_one(id, product)
    return resolve
