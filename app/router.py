from typing import Annotated
from fastapi import APIRouter, Depends

from app.repository import ProductRepo
from app.schemas import SProduct, SProductAdd, SProductId

router = APIRouter(
    prefix='/products',
    tags=['products']
)


@router.get('')
async def get_products() -> list[SProduct]:
    products = await ProductRepo.find_all()
    return products


@router.post('')
async def add_products(product: Annotated[SProductAdd, Depends()]) -> SProductId:
    product_id = await ProductRepo.add_one(product)
    return {'ok': True, 'product_id': product_id}
