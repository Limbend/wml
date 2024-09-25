from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

from backend.database import str_50, str_255, num_9_2


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


class SResolve(BaseModel):
    ok: bool = True
    product_id: int
    message: Optional[str] = None


class SPagination(BaseModel):
    limit: int = Field(25, ge=1, le=100)
    offset: int = Field(0, ge=0)
