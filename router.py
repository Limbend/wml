from typing import Annotated
from fastapi import APIRouter, Depends

from repository import ProductRepo
from schemas import SProduct, SProductAdd, SProductId

router = APIRouter(
    prefix='/products',
    tags=['products']
)


@router.get('')
async def get_products() -> SProduct:
    products = await ProductRepo.find_all()

    return {"products": products}


@router.post('')
async def add_products(product: Annotated[SProductAdd, Depends()]) -> SProductId:
    product_id = await ProductRepo.add_one(product)

    return {'ok': True, 'product_id': product_id}
