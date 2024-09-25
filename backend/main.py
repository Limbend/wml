from datetime import datetime
from fastapi import FastAPI
from contextlib import asynccontextmanager

from backend.repository import ProductRepo
from backend.router import router as product_router
from backend.database import create_tables, delete_tables
from backend.schemas import SProductAdd


@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    print("База очищена")
    await create_tables()
    await ProductRepo.add_one(SProductAdd(name='lamp', price=179.99, buy_date=datetime.now()))
    await ProductRepo.add_one(SProductAdd(name='ipod', price=20, buy_date=datetime.now()))
    await ProductRepo.add_one(SProductAdd(name='spoon', price=475.50, buy_date=datetime.now()))
    print("База готова к работе")
    yield
    print("Выключение")

app = FastAPI(title="WML", lifespan=lifespan)
app.include_router(product_router)
