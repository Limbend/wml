
from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class SProductAdd(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    price: Optional[float] = None
    model: Optional[str] = None
    is_purchased: bool = False
    buy_date: Optional[datetime] = None
    guarantee: Optional[int] = None
    guarantee_end_date: Optional[datetime] = None
    receipt: Optional[str] = None
    shop: Optional[str] = None
    priority: Optional[int] = None


class SProduct(SProductAdd):
    id: int


class SProductId(BaseModel):
    ok: bool = True
    product_id: int
