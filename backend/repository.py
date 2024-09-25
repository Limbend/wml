from sqlalchemy import select, update

from backend.schemas import SProductAdd, SProduct, SResolve
from backend.database import ProductOrm, new_session


class ProductRepo:
    @classmethod
    async def add_one(cls, data: SProductAdd) -> SResolve:
        async with new_session() as session:
            product = ProductOrm(**data.model_dump())
            session.add(product)
            await session.flush()
            await session.commit()
            return SResolve(product_id=product.id)

    @classmethod
    async def find_all(cls) -> list[SProduct]:
        async with new_session() as session:
            query = select(ProductOrm)
            result = await session.execute(query)
            product_shchemas = [SProduct.model_validate(
                product_model) for product_model in result.scalars().all()]
            return product_shchemas

    @classmethod
    async def update_one(cls, id: int, data: dict) -> SResolve:
        async with new_session() as session:
            query = update(ProductOrm).values(**data).filter_by(id=id)
            print(query.compile(compile_kwargs={'literal_binds': True}))
            await session.execute(query)
            await session.commit()

        return SResolve(product_id=id)

    @classmethod
    async def replase_one(cls, id: int, data: SProductAdd) -> SResolve:
        return cls.update_one(id, data.model_dump())
