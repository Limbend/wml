

from sqlalchemy import select
from schemas import SProductAdd
from database import ProductOrm, new_session


class ProductRepo:
    @classmethod
    async def add_one(cls, data: SProductAdd) -> int:
        async with new_session() as session:
            product_dict = data.model_dump()

            product = ProductOrm(**product_dict)
            session.add(product)
            await session.flush()
            await session.commit()
            return product.id

    @classmethod
    async def find_all(cls):
        async with new_session() as session:
            query = select(ProductOrm)
            result = await session.execute(query)
            product_models = result.scalars().all()
            return product_models
