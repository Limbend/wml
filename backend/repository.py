import logging
from sqlalchemy import func, select, update

from schemas import SProductAdd, SProductEdit, SProduct, SProductList, SResponseAdd, SResponseUpdate, SPagination, SSort
from models import ProductOrm

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


from config import settings

logger = logging.getLogger(__name__)
engine = create_async_engine(
    settings.db.connection_url,
    echo=True,
)
new_session = async_sessionmaker(engine, expire_on_commit=False)


class ProductRepo:
    @classmethod
    async def add_one(cls, data: SProductAdd) -> SResponseAdd:
        auto_generated_fields = data.auto_generate_fields()

        async with new_session() as session:
            product = ProductOrm(**data.model_dump())
            session.add(product)
            await session.flush()
            await session.commit()
            return SResponseAdd(product_id=product.id, auto_generated_fields=auto_generated_fields)

    @classmethod
    async def get_list(cls, padding: SPagination, sorting: SSort) -> SProductList:
        async with new_session() as session:
            query = select(func.count(ProductOrm.id))
            result = await session.execute(query)
            total_count = result.scalar()

            query = select(ProductOrm)
            if sorting.desc:
                query = query.order_by(
                    getattr(ProductOrm, sorting.field.value).desc())
            else:
                query = query.order_by(
                    getattr(ProductOrm, sorting.field.value).asc())

            query = query.offset(padding.get_offset()).limit(padding.by)

            result = await session.execute(query)
            product_shchemas = [SProduct.model_validate(
                product_model) for product_model in result.scalars().all()]

            return SProductList(products=product_shchemas, total_count=total_count)

    @classmethod
    async def edit_one(cls, product: SProductEdit) -> SResponseUpdate:
        async with new_session() as session:
            query = select(ProductOrm).filter_by(id=product.id)
            # logger.info(query.compile(compile_kwargs={'literal_binds': True}))
            result = await session.execute(query)
            product_in_db = SProduct.model_validate(result.scalar())

            product.auto_generate_fields(product_in_db)
            edit_fields = product.get_edit_fields()
            updated_product = product_in_db.model_copy(update=edit_fields)

            query = update(ProductOrm).values(
                **edit_fields).filter_by(id=product.id)
            # logger.info(query.compile(compile_kwargs={'literal_binds': True}))
            await session.execute(query)

            await session.commit()

        return SResponseUpdate(updated_product=updated_product)
