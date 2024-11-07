import logging
from sqlalchemy import func, select, update, or_, String
from sqlalchemy.sql.expression import cast


from schemas import (
    SBaseResponse,
    SProductAdd,
    SProductEdit,
    SProduct,
    SPagination,
    SResponseAdd,
    SResponseGet,
    SResponseUpdate,
    SSort,
)
from models import ProductOrm

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


from config import settings

logger = logging.getLogger(__name__)
engine = create_async_engine(
    settings.db.connection_url,
    echo=settings.db.echo,
)
new_session = async_sessionmaker(engine, expire_on_commit=False)


class ProductRepo:
    @classmethod
    async def add_one(cls, data: SProductAdd) -> SResponseAdd:
        async with new_session() as session:
            product = ProductOrm(**data.model_dump())
            session.add(product)
            await session.flush()
            await session.commit()
            return SResponseAdd(
                content=SResponseAdd.ContentAdd(
                    product_id=product.id,
                    auto_generated_fields=data.generated_fields,
                )
            )

    @classmethod
    async def hide_one(cls, product_id: int) -> SBaseResponse:
        async with new_session() as session:
            query = update(ProductOrm).values(is_hidden=True).filter_by(id=product_id)
            await session.execute(query)
            await session.commit()
        return SBaseResponse()

    @classmethod
    async def get_list(cls, padding: SPagination, sorting: SSort) -> SResponseGet:
        async with new_session() as session:
            query = select(func.count(ProductOrm.id)).filter_by(is_hidden=False)
            result = await session.execute(query)
            total_count = result.scalar()

            query = select(ProductOrm).filter_by(is_hidden=False)
            if sorting.desc:
                query = query.order_by(getattr(ProductOrm, sorting.field.value).desc())
            else:
                query = query.order_by(getattr(ProductOrm, sorting.field.value).asc())

            query = query.offset(padding.get_offset()).limit(padding.by)

            result = await session.execute(query)
            product_shchemas = [
                SProduct.model_validate(product_model)
                for product_model in result.scalars().all()
            ]

            return SResponseGet(total_count=total_count, content=product_shchemas)

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

            query = update(ProductOrm).values(**edit_fields).filter_by(id=product.id)
            # logger.info(query.compile(compile_kwargs={'literal_binds': True}))
            await session.execute(query)

            await session.commit()

        return SResponseUpdate(content=updated_product)

    @classmethod
    async def search(cls, search_str: str, padding: SPagination) -> SResponseGet:
        search_str = f"%{search_str}%"

        def f_search_query(s):
            return (
                select(s)
                .filter(
                    or_(
                        ProductOrm.name.like(search_str),
                        ProductOrm.model.like(search_str),
                        ProductOrm.shop.like(search_str),
                        cast(ProductOrm.price, String).like(search_str),
                        cast(ProductOrm.buy_date, String).like(search_str),
                        cast(ProductOrm.guarantee, String).like(search_str),
                        cast(ProductOrm.guarantee_end_date, String).like(search_str),
                    )
                )
                .filter_by(is_hidden=False)
            )

        async with new_session() as session:
            query = f_search_query(func.count(ProductOrm.id))

            result = await session.execute(query)
            total_count = result.scalar()

            query = (
                f_search_query(ProductOrm)
                .order_by(
                    ProductOrm.name.like(search_str).desc(),
                    ProductOrm.model.like(search_str).desc(),
                    ProductOrm.shop.like(search_str).desc(),
                    cast(ProductOrm.price, String).like(search_str).desc(),
                    cast(ProductOrm.buy_date, String).like(search_str).desc(),
                    cast(ProductOrm.guarantee, String).like(search_str).desc(),
                    cast(ProductOrm.guarantee_end_date, String).like(search_str).desc(),
                    ProductOrm.id.desc(),
                )
                .offset(padding.get_offset())
                .limit(padding.by)
            )

            result = await session.execute(query)
            product_shchemas = [
                SProduct.model_validate(product_model)
                for product_model in result.scalars().all()
            ]

        return SResponseGet(total_count=total_count, content=product_shchemas)
