from typing import Annotated
from fastapi import APIRouter, Body, Depends, File, UploadFile

from repository import ProductRepo
from schemas import (
    ReceiptValidator,
    SBaseResponse,
    SProductEdit,
    SPagination,
    SProductAdd,
    SResponseAdd,
    SResponseAddReceipt,
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


@router.get("/search")
async def search_products(
    search_query: str, padding: Annotated[SPagination, Depends()]
) -> SResponseGet:
    products = await ProductRepo.search(search_query, padding)
    return products


@router.post("/receipts")
async def upload_receipt(
    product_id: int,
    file: UploadFile = File(...),
) -> SResponseAddReceipt:
    ReceiptValidator().validate(file)
    resolve = await ProductRepo.upload_receipt(product_id, file)
    return resolve
