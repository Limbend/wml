import logging
from sqlalchemy import func, select, update, or_, String
from sqlalchemy.orm import joinedload
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
    SShop,
    SSort,
)
from models import ProductOrm, ShopOrm

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
            if "__shop_name__" in data.generated_fields.keys():
                await cls._create_and_set_shop_(
                    session, data.generated_fields["__shop_name__"], product
                )

            session.add(product)
            await session.flush()
            await session.commit()

            if "__shop_name__" in data.generated_fields.keys():
                data.generated_fields["shop"] = SShop.model_validate(
                    product.shop
                ).model_dump()
                del data.generated_fields["__shop_name__"]

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

            query = (
                select(ProductOrm)
                .options(joinedload(ProductOrm.shop))
                .filter_by(is_hidden=False)
            )
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
    async def edit_one(cls, data: SProductEdit) -> SResponseUpdate:
        async with new_session() as session:
            query = (
                select(ProductOrm)
                .options(joinedload(ProductOrm.shop))
                .filter_by(id=data.id)
            )
            # logger.info(query.compile(compile_kwargs={'literal_binds': True}))
            result = await session.execute(query)
            product_in_db = SProduct.model_validate(result.scalar())

            data.auto_generate_fields(product_in_db)
            if "__shop_name__" in data.generated_fields.keys():
                await cls._create_and_set_shop_(
                    session, data.generated_fields["__shop_name__"], product_in_db
                )
                await session.flush()

            edit_fields = data.get_edit_fields(product_in_db)
            query = update(ProductOrm).values(**edit_fields).filter_by(id=data.id)
            # logger.info(query.compile(compile_kwargs={'literal_binds': True}))
            await session.execute(query)
            await session.commit()

        updated_product = product_in_db.model_copy(update=edit_fields)
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
                        ProductOrm.product_link.like(search_str),
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
                .options(joinedload(ProductOrm.shop))
                .order_by(
                    ProductOrm.name.like(search_str).desc(),
                    ProductOrm.model.like(search_str).desc(),
                    ProductOrm.product_link.like(search_str).desc(),
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

    @classmethod
    async def _create_and_set_shop_(
        cls, session, shop_name: str, target_product: ProductOrm
    ):
        query = select(ShopOrm).filter_by(name=shop_name)
        result = await session.execute(query)
        result = result.scalar()

        if result is not None:
            target_product.shop_id = result.id
            target_product.shop = result
        else:
            shop = ShopOrm(name=shop_name)
            target_product.shop = shop
            session.add(shop)
