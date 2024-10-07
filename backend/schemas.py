from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from pydantic.json_schema import SkipJsonSchema
from datetime import date
from dateutil.relativedelta import relativedelta
from enum import Enum

from models import str_50, str_255, num_9_2


class SProductAdd(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str_50 = Field(min_length=1, max_length=50)
    model: Optional[str_255] = Field(None, max_length=255)
    price: Optional[num_9_2] = Field(None, max_digits=9, decimal_places=2, gt=0)
    is_purchased: bool = False
    buy_date: Optional[date] = None
    guarantee: int = Field(None, ge=0)
    guarantee_end_date: SkipJsonSchema[date] = None
    receipt: Optional[str] = None
    shop: Optional[str_255] = Field(None, max_length=255)
    priority: int = Field(None, ge=1, le=10)
    is_hidden: SkipJsonSchema[bool] = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.auto_generate_fields()

    def auto_generate_fields(self) -> dict:
        fields = {}
        if self.guarantee is None:
            self.guarantee = 0
            fields.update({"guarantee": self.guarantee})
        if self.priority is None:
            self.priority = 5
            fields.update({"priority": self.priority})

        if self.buy_date is not None:
            self.guarantee_end_date = self.buy_date + relativedelta(
                months=+self.guarantee
            )
            fields.update({"guarantee_end_date": self.guarantee_end_date})

        self._generated_fields_ = fields

        return self._generated_fields_

    @property
    def generated_fields(self):
        return self._generated_fields_


class SProduct(SProductAdd):
    id: int = Field(gt=0)
    guarantee_end_date: Optional[date] = None
    is_hidden: bool = False


class SProductEdit(SProductAdd):
    id: int = Field(gt=0)
    name: Optional[str_50] = Field(None, min_length=1, max_length=50)
    is_purchased: Optional[bool] = None
    guarantee: Optional[int] = Field(None, ge=0)
    priority: Optional[int] = Field(None, ge=1, le=10)

    def __init__(self, **kwargs):
        BaseModel.__init__(self, **kwargs)

    def auto_generate_fields(self, product_in_db: SProduct):
        fields = {}
        buy_date = (
            self.buy_date if self.buy_date is not None else product_in_db.buy_date
        )
        guarantee = (
            self.guarantee if self.guarantee is not None else product_in_db.guarantee
        )

        if buy_date is not None and guarantee is not None:
            guarantee_end_date = buy_date + relativedelta(months=+guarantee)
            if guarantee_end_date != product_in_db.guarantee_end_date:
                self.guarantee_end_date = guarantee_end_date
                fields.update({"guarantee_end_date": self.guarantee_end_date})

        self._generated_fields_ = fields
        return self._generated_fields_

    def get_edit_fields(self):
        edit_fields = self.model_dump()

        edit_fields = {
            key: edit_fields[key]
            for key in edit_fields.keys()
            if key != "id" and not edit_fields[key] is None
        }

        return edit_fields


class SResponse(BaseModel):
    ok: bool = True
    message: Optional[str] = None


class SResponseAdd(SResponse):
    product_id: Optional[int] = None
    auto_generated_fields: dict = {}


class SResponseUpdate(SResponse):
    updated_product: Optional[SProduct] = None


class SPagination(BaseModel):
    by: int = Field(25, ge=1, le=100)
    chunk: int = Field(0, ge=0)

    def get_offset(self):
        return self.chunk * self.by


class ProductSortingField(Enum):
    id = "id"
    name = "name"
    buy_date = "buy_date"
    guarantee = "guarantee"
    guarantee_end_date = "guarantee_end_date"
    shop = "shop"
    priority = "priority"


class SSort(BaseModel):
    field: Optional[ProductSortingField] = ProductSortingField.id
    desc: Optional[bool] = False


class SProductList(BaseModel):
    products: list[SProduct]
    total_count: int
