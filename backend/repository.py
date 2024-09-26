from pydantic import Field
from sqlalchemy import func, select, update

from backend.schemas import SProductAdd, SProduct, SProductList, SResponseAdd, SResponseUpdate, SPagination
from backend.database import ProductOrm, new_session


class ProductRepo:
    @classmethod
    async def add_one(cls, data: SProductAdd) -> SResponseAdd:
        async with new_session() as session:
            product = ProductOrm(**data.model_dump())
            session.add(product)
            await session.flush()
            await session.commit()
            return SResponseAdd(product_id=product.id)

    @classmethod
    async def get_list(cls, padding: SPagination) -> SProductList:
        async with new_session() as session:
            query = select(func.count(ProductOrm.id))
            result = await session.execute(query)
            count = result.scalar()

            query = select(ProductOrm).order_by(ProductOrm.id.asc()).offset(
                padding.offset).limit(padding.limit)
            result = await session.execute(query)
            product_shchemas = [SProduct.model_validate(
                product_model) for product_model in result.scalars().all()]

            return SProductList(products=product_shchemas, count=count)

    @classmethod
    async def update_one(cls, id: int, data: dict) -> SResponseUpdate:
        async with new_session() as session:
            query = update(ProductOrm).values(**data).filter_by(id=id)
            # print(query.compile(compile_kwargs={'literal_binds': True}))
            await session.execute(query)

            query = select(ProductOrm).filter_by(id=id)
            result = await session.execute(query)
            product_shchemas = SProduct.model_validate(result.scalar())

            await session.commit()

        return SResponseUpdate(updated_product=product_shchemas)

    @classmethod
    async def replase_one(cls, id: int, data: SProductAdd) -> SResponseUpdate:
        return cls.update_one(id, data.model_dump())
