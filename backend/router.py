from typing import Annotated
from fastapi import APIRouter, Depends
from pydantic import ValidationError

from backend.repository import ProductRepo
from backend.schemas import SProduct, SProductAdd, SResolve

router = APIRouter(
    prefix='/products',
    tags=['products']
)


@router.get('')
async def get_products() -> list[SProduct]:
    products = await ProductRepo.find_all()
    return products


@router.post('')
async def add_products(product: Annotated[SProductAdd, Depends()]) -> SResolve:
    resolve = await ProductRepo.add_one(product)

    return resolve


@router.patch('')
async def update_one(id: int, data: dict) -> SResolve:
    resolve = await ProductRepo.update_one(id, data)
    return resolve


@router.put('')
async def edit_products(id: int, product: Annotated[SProductAdd, Depends()]) -> SResolve:
    resolve = await ProductRepo.replase_one(id, product)
    return resolve
