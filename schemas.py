
from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class SProductAdd(BaseModel):
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


class SProductGet(SProductAdd):
    id: int
