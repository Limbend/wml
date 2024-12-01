import logging
from typing import Optional, List, Union
from fastapi import HTTPException
from starlette import status
from pydantic import BaseModel, ConfigDict, Field
from pydantic.json_schema import SkipJsonSchema
from datetime import date
from dateutil.relativedelta import relativedelta
from enum import Enum
import re

from models import str_50, str_256, str_1024, str_2048, num_9_2

logger = logging.getLogger(__name__)


class SShop(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(gt=0)
    name: str_256 = Field(max_length=256)


class SProductAdd(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str_50 = Field(min_length=1, max_length=50)
    model: Optional[str_256] = Field(None, max_length=256)
    price: Optional[num_9_2] = Field(None, max_digits=9, decimal_places=2, gt=0)
    is_purchased: bool = False
    buy_date: Optional[date] = None
    guarantee: int = Field(None, ge=0)
    guarantee_end_date: SkipJsonSchema[date] = None
    receipt: Optional[str_1024] = Field(None, max_length=1024)
    product_link: Optional[str_2048] = Field(None, max_length=2048)
    priority: int = Field(None, ge=1, le=10)
    is_hidden: SkipJsonSchema[bool] = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.auto_generate_fields()

    @staticmethod
    def get_url_in_str(source_str: str):
        pattern = "(https:\/\/|http:\/\/|www.)[a-z0-9/\.,\-+=_?&~!*'();:@&$]+"
        url = re.search(pattern, source_str.lower())
        if url is not None:
            return url.group()
        return False

    @staticmethod
    def get_domain_in_url(url: str):
        pattern = "\/\/[a-z0-9\.\-+=_]+\/"
        domain = re.search(pattern, url.lower())
        if domain is not None:
            domain = domain.group()[2:-1]
            if "www." == domain[:4]:
                domain = domain[4:]
            return domain
        return False

    def auto_generate_fields(self) -> dict:
        self._generated_fields_ = {}
        if self.guarantee is None:
            self.guarantee = 0
            self._generated_fields_.update({"guarantee": self.guarantee})
        if self.priority is None:
            self.priority = 5
            self._generated_fields_.update({"priority": self.priority})

        if self.buy_date is not None:
            self.guarantee_end_date = self.buy_date + relativedelta(
                months=+self.guarantee
            )
            self._generated_fields_.update(
                {"guarantee_end_date": self.guarantee_end_date}
            )

        if self.product_link is not None:
            new_product_link = self.get_url_in_str(self.product_link)
            if new_product_link:
                if new_product_link != self.product_link:
                    self.product_link = new_product_link
                    self._generated_fields_.update({"product_link": self.product_link})

                shop_name = self.get_domain_in_url(self.product_link)
                if shop_name:
                    self._generated_fields_.update({"__shop_name__": shop_name})

        return self._generated_fields_

    @property
    def generated_fields(self):
        return self._generated_fields_


class SProductWithoutShop(SProductAdd):
    id: int = Field(gt=0)
    guarantee_end_date: Optional[date] = None
    is_hidden: bool = False


class SProduct(SProductWithoutShop):
    shop: Optional[SShop] = None


class SProductEdit(SProductAdd):
    id: int = Field(gt=0)
    name: Optional[str_50] = Field(None, min_length=1, max_length=50)
    is_purchased: Optional[bool] = None
    guarantee: Optional[int] = Field(None, ge=0)
    priority: Optional[int] = Field(None, ge=1, le=10)

    def __init__(self, **kwargs):
        BaseModel.__init__(self, **kwargs)

    def auto_generate_fields(self, product_in_db: SProduct):
        self._generated_fields_ = {}
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
                self._generated_fields_.update(
                    {"guarantee_end_date": self.guarantee_end_date}
                )

        if (
            self.product_link is not None
            and self.product_link != product_in_db.product_link
        ):
            new_product_link = self.get_url_in_str(self.product_link)
            if new_product_link:
                if new_product_link != self.product_link:
                    self.product_link = new_product_link
                    self._generated_fields_.update({"product_link": self.product_link})

                shop_name = self.get_domain_in_url(self.product_link)
                if shop_name:
                    self._generated_fields_.update({"__shop_name__": shop_name})

        return self._generated_fields_

    def get_edit_fields(self, product_in_db: SProduct):
        edit_fields = self.model_dump()
        old_fields = product_in_db.model_dump()

        edit_fields = {
            key: edit_fields[key]
            for key in edit_fields.keys()
            if key != "id"
            and not edit_fields[key] is None
            and edit_fields[key] != old_fields[key]
        }

        if "__shop_name__" in self._generated_fields_:
            edit_fields.update({"shop_id": product_in_db.shop.id})
            del self.generated_fields["__shop_name__"]

        return edit_fields


class SBaseResponse(BaseModel):
    ok: bool = True
    message: Optional[str] = None


class SResponseAdd(SBaseResponse):
    class ContentAdd(BaseModel):
        product_id: Optional[int] = None
        auto_generated_fields: dict = {}

    content: ContentAdd


class SResponseUpdate(SBaseResponse):
    content: Optional[SProduct] = None


class SResponseGet(SBaseResponse):
    total_count: Optional[int] = None
    content: Optional[list[SProduct]] = None


class SResponseAddReceipt(SBaseResponse):
    content: Optional[str] = None


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
    product_link = "product_link"
    priority = "priority"


class SSort(BaseModel):
    field: Optional[ProductSortingField] = ProductSortingField.id
    desc: Optional[bool] = False


class BaseFileValidator:
    def __init__(
        self,
        size_limit: int = None,
        content_type: Union[List[str], str] = None,
    ):
        self.size_limit = size_limit
        if type(content_type) == list:
            self.content_type = content_type
        else:
            self.content_type = [content_type]

    def validate(self, file):
        if self.size_limit is not None and file.size > self.size_limit:
            message = f"File size is too large. The maximum size is {self.size_limit}."
            logger.error(message)
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=message,
            )

        if file.content_type is not None:
            if (
                self.content_type is not None
                and file.content_type not in self.content_type
            ):
                message = f"File type ({file.content_type}) is not supported. Valid file types: {self.content_type}."
                logger.error(message)
                raise HTTPException(
                    status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                    detail=message,
                )
        else:
            # Check the file by ext if there are no headers.
            file_ext = file.filename.split(".")[-1]
            valid_ext = [c_type.split("/")[-1] for c_type in self.content_type]
            if file_ext not in valid_ext:
                message = f"File type ({file_ext}) is not supported. Valid file types: {valid_ext}."
                logger.error(message)
                raise HTTPException(
                    status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                    detail=message,
                )

        return True


class ReceiptValidator(BaseFileValidator):
    size_limit = 15_728_640
    content_type = [
        "application/pdf",
        "image/jpeg",
        "image/jpg",
        "image/png",
    ]

    def __init__(self):
        super().__init__(self.size_limit, self.content_type)
