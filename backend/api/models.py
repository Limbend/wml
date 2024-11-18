from decimal import Decimal
from typing import Annotated, Optional
from pydantic import PlainSerializer
from sqlalchemy import CheckConstraint, Numeric, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import date

intpk = Annotated[int, mapped_column(primary_key=True)]
str_50 = Annotated[str, 50]
str_256 = Annotated[str, 256]
str_2048 = Annotated[str, 2048]
num_9_2 = Annotated[
    Decimal, PlainSerializer(lambda x: float(x), return_type=float, when_used="json")
]


class Base(DeclarativeBase):
    __table_args__ = {"schema": "backend"}

    type_annotation_map = {
        str_50: String(50),
        str_256: String(256),
        str_2048: String(2048),
        num_9_2: Numeric(9, 2),
    }

    repr_cols_num = 3
    repr_cols = tuple()

    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"


class ShopOrm(Base):
    __tablename__ = "shops"
    id: Mapped[intpk]
    name: Mapped[Optional[str_256]]
    # alias_id: Mapped[Optional[int]] = mapped_column(ForeignKey("shops.id"))

    product: Mapped["ProductOrm"] = relationship(back_populates="shop")

    __table_args__ = (UniqueConstraint("name"), {"schema": "backend"})


class ProductOrm(Base):
    __tablename__ = "products"

    id: Mapped[intpk]
    name: Mapped[str_50]
    model: Mapped[Optional[str_256]]
    price: Mapped[Optional[num_9_2]]
    is_purchased: Mapped[bool]
    buy_date: Mapped[Optional[date]]
    guarantee: Mapped[int]
    guarantee_end_date: Mapped[Optional[date]]
    receipt: Mapped[Optional[str]]
    product_link: Mapped[Optional[str_2048]]
    shop_id: Mapped[Optional[int]] = mapped_column(ForeignKey(ShopOrm.id))
    priority: Mapped[int]
    is_hidden: Mapped[bool]

    shop: Mapped[Optional["ShopOrm"]] = relationship(back_populates="product")
