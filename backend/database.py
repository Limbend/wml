from decimal import Decimal
from typing import Annotated, Optional
from sqlalchemy import Numeric, String
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime

from backend.config import settings

engine = create_async_engine(
    settings.DATABASE_URL_asyncpg,
    echo=True,
)
new_session = async_sessionmaker(engine, expire_on_commit=False)


intpk = Annotated[int, mapped_column(primary_key=True)]
str_50 = Annotated[str, 50]
str_255 = Annotated[str, 255]
num_9_2 = Annotated[Decimal, 9]


class Base(DeclarativeBase):
    __table_args__ = {"schema": "backend"}

    type_annotation_map = {
        str_50: String(50),
        str_255: String(255),
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


class ProductOrm(Base):
    __tablename__ = "products"

    id: Mapped[intpk]
    name: Mapped[str_50]
    price: Mapped[Optional[num_9_2]]
    model: Mapped[Optional[str_255]]
    is_purchased: Mapped[bool]
    buy_date: Mapped[Optional[datetime]]
    guarantee: Mapped[int]
    guarantee_end_date: Mapped[Optional[datetime]]
    receipt: Mapped[Optional[str]]
    shop: Mapped[Optional[str_255]]
    priority: Mapped[Optional[int]]


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
