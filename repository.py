from sqlalchemy import select

from schemas import SProductAdd, SProduct
from database import ProductOrm, new_session


class ProductRepo:
    @classmethod
    async def add_one(cls, data: SProductAdd) -> int:
        async with new_session() as session:
            product = ProductOrm(**data.model_dump())
            session.add(product)
            await session.flush()
            await session.commit()
            return product.id

    @classmethod
    async def find_all(cls) -> list[SProduct]:
        async with new_session() as session:
            query = select(ProductOrm)
            result = await session.execute(query)
            product_shchemas = [SProduct.model_validate(
                product_model) for product_model in result.scalars().all()]
            return product_shchemas
