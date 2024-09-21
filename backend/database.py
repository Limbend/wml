from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime

engine = create_async_engine('sqlite+aiosqlite:///temp/products.db')
new_session = async_sessionmaker(engine, expire_on_commit=False)


class Model(DeclarativeBase):
    pass


class ProductOrm(Model):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    price: Mapped[float | None]
    model: Mapped[str | None]
    is_purchased: Mapped[bool]
    buy_date: Mapped[datetime | None]
    guarantee: Mapped[int | None]
    guarantee_end_date: Mapped[datetime | None]
    receipt: Mapped[str | None]
    shop: Mapped[str | None]
    priority: Mapped[int | None]


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
