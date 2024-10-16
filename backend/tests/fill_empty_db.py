from datetime import datetime
import asyncio
import logging
from logging import config as lc
import os
import sys

sys.path.append(os.path.join(sys.path[0], ".."))
sys.path.append(os.path.join(sys.path[0], "../api"))

from api.config import settings
from api.repository import ProductRepo
from api.schemas import SPagination, SProductAdd, SSort


lc.dictConfig(settings.logging_config)
logger = logging.getLogger("tests.fill_empty_db")

products = [
    SProductAdd(
        name="Smartphone",
        price=699.99,
        model="Galaxy S21",
        is_purchased=True,
        buy_date=datetime.strptime("2022-03-15", "%Y-%m-%d").date(),
        guarantee=24,
        receipt="https://example.com/receipt1",
        shop="Best Buy",
        priority=1,
    ),
    SProductAdd(
        name="Laptop",
        price=1299.99,
        model="MacBook Pro 16",
        is_purchased=True,
        buy_date=datetime.strptime("2023-01-10", "%Y-%m-%d").date(),
        guarantee=12,
        receipt="https://example.com/receipt2",
        shop="Apple Store",
        priority=2,
    ),
    SProductAdd(
        name="Bluetooth Speaker",
        price=149.99,
        model="JBL Charge 4",
        is_purchased=True,
        buy_date=datetime.strptime("2021-08-05", "%Y-%m-%d").date(),
        guarantee=12,
        receipt="https://example.com/receipt3",
        shop="Amazon",
        priority=3,
    ),
    SProductAdd(
        name="Headphones",
        model="Sony WH-1000XM4",
        is_purchased=False,
        priority=4,
    ),
    SProductAdd(
        name="Camera",
        price=999.99,
        model="Canon EOS R",
        is_purchased=True,
        buy_date=datetime.strptime("2022-11-22", "%Y-%m-%d").date(),
        guarantee=24,
        receipt="https://example.com/receipt5",
        shop="B&H",
        priority=2,
    ),
    SProductAdd(
        name="Gaming Console",
        price=499.99,
        model="PlayStation 5",
        is_purchased=False,
        priority=1,
    ),
    SProductAdd(
        name="Smartwatch",
        price=249.99,
        model="Apple Watch Series 7",
        is_purchased=True,
        buy_date=datetime.strptime("2023-02-15", "%Y-%m-%d").date(),
        guarantee=12,
        receipt="https://example.com/receipt7",
        shop="Apple Store",
        priority=3,
    ),
    SProductAdd(
        name="Tablet",
        price=799.99,
        model="iPad Pro 11",
        is_purchased=True,
        buy_date=datetime.strptime("2023-06-12", "%Y-%m-%d").date(),
        guarantee=12,
        receipt="https://example.com/receipt8",
        shop="Apple Store",
        priority=2,
    ),
    SProductAdd(
        name="Monitor",
        price=399.99,
        model="Dell UltraSharp 27",
        is_purchased=True,
        buy_date=datetime.strptime("2022-09-30", "%Y-%m-%d").date(),
        guarantee=24,
        receipt="https://example.com/receipt9",
        shop="Dell Store",
        priority=3,
    ),
    SProductAdd(
        name="Keyboard",
        price=99.99,
        model="Logitech MX Keys",
        is_purchased=True,
        buy_date=datetime.strptime("2023-04-01", "%Y-%m-%d").date(),
        guarantee=12,
        receipt="https://example.com/receipt10",
        shop="Amazon",
        priority=4,
    ),
]


async def main():
    responce = await ProductRepo.get_list(SPagination(), SSort())

    logger.info(f"DB total_count: {responce.total_count}")

    if responce.total_count == 0:
        logger.info(f"Filling the database with {len(products)} records.")
        for product in products:
            responce = await ProductRepo.add_one(product)
            logger.info(responce)

        logger.info("Filling is complete")


if __name__ == "__main__":
    asyncio.run(main())
