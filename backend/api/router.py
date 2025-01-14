import logging
from typing import Annotated, Optional
from contextlib import asynccontextmanager
from fastapi import (
    APIRouter,
    HTTPException,
    Body,
    Depends,
    File,
    UploadFile,
    status,
)

from repository import ProductRepo
from schemas import (
    ReceiptValidator,
    SProductEdit,
    SPagination,
    SProductAdd,
    SResponseAdd,
    SResponseAddReceipt,
    SResponseGet,
    SResponseUpdate,
    SSort,
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: APIRouter):
    logger.info(f"Product router STARTING")
    await ProductRepo.check_db_connection()
    yield
    logger.info(f"Product router SHUTDOWN")


router = APIRouter(prefix="/products", tags=["products"], lifespan=lifespan)


@router.get("")
async def get_products(
    padding: Annotated[SPagination, Depends()],
    sorting: Annotated[SSort, Depends()],
    search_query: Optional[str] = None,
) -> SResponseGet:
    if search_query is None:
        products = await ProductRepo.get_list(padding, sorting)
    else:
        products = await ProductRepo.search(search_query, padding, sorting)

    return products


@router.post("")
async def add_products(product: Annotated[SProductAdd, Body()]) -> SResponseAdd:
    response = await ProductRepo.add_one(product)
    return response


@router.delete("")
async def del_products(
    product_id: int,
    padding: Annotated[SPagination, Depends()],
    sorting: Annotated[SSort, Depends()],
) -> SResponseGet:
    hide_response = await ProductRepo.hide_one(product_id=product_id)

    if not hide_response.ok:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The product has not been updated! This id ({product_id}) does not exist or it was deleted earlier.",
        )

    # Returns the product, to replace the deleted.
    padding.chunk = padding.chunk + 1
    selector = SPagination(by=1, chunk=padding.get_offset() - 1)
    replacement_product = await ProductRepo.get_list(selector, sorting)

    return replacement_product


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
                        "model": "super pro max extra ++",
                        "price": 50.01,
                        "buy_date": "2024-09-29",
                    },
                },
                "all": {
                    "summary": "All fields",
                    "description": "Completely rewrite the product, replacing all fields.",
                    "value": {
                        "id": 1,
                        "name": "Gamer's spoon",
                        "model": "super pro max extra ++",
                        "price": 50.01,
                        "is_purchased": False,
                        "buy_date": "2024-09-29",
                        "guarantee": 2,
                        "receipt": "string",
                        "product_link": "https://amazon.com/example-product",
                        "priority": 1,
                    },
                },
            }
        ),
    ],
) -> SResponseUpdate:
    response = await ProductRepo.edit_one(edit_product)
    return response


@router.post("/receipts")
async def upload_receipt(
    product_id: int,
    file: UploadFile = File(...),
) -> SResponseAddReceipt:
    ReceiptValidator().validate(file)
    resolve = await ProductRepo.upload_receipt(product_id, file)
    return resolve
