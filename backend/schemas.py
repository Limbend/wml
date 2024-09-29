from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from enum import Enum

from models import str_50, str_255, num_9_2


class SProductAdd(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str_50 = Field(min_length=1, max_length=50)
    price: Optional[num_9_2] = Field(
        None, max_digits=9, decimal_places=2, gt=0)
    model: Optional[str_255] = Field(None, max_length=255)
    is_purchased: bool = False
    buy_date: Optional[datetime] = None
    guarantee: int = Field(0, ge=0)
    receipt: Optional[str] = None
    shop: Optional[str_255] = Field(None, max_length=255)
    priority: Optional[int] = Field(None, ge=0)


class SProduct(SProductAdd):
    id: int = Field(gt=0)
    guarantee_end_date: Optional[datetime] = None


class SResponse(BaseModel):
    ok: bool = True
    message: Optional[str] = None


class SResponseAdd(SResponse):
    product_id: Optional[int] = None


class SResponseUpdate(SResponse):
    updated_product: Optional[SProduct] = None


class SPagination(BaseModel):
    by: int = Field(25, ge=1, le=100)
    chunk: int = Field(0, ge=0)

    def get_offset(self):
        return self.chunk * self.by


class ProductSortingField(Enum):
    id = 'id'
    name = 'name'
    buy_date = 'buy_date'
    guarantee = 'guarantee'
    guarantee_end_date = 'guarantee_end_date'
    shop = 'shop'
    priority = 'priority'


class SSort(BaseModel):
    field: Optional[ProductSortingField] = ProductSortingField.id
    desc: Optional[bool] = False


class SProductList(BaseModel):
    products: list[SProduct]
    total_count: int
