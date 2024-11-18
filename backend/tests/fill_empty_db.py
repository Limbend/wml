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
        product_link="Best Buy",
        priority=1,
    ),
    SProductAdd(
        name="Laptop",
        price=2499.00,
        model="MacBook Pro 16",
        is_purchased=True,
        buy_date=datetime.strptime("2024-11-10", "%Y-%m-%d").date(),
        guarantee=12,
        receipt="https://example.com/receipt2",
        product_link="https://www.apple.com/shop/buy-mac/macbook-pro/16-inch-space-black-standard-display-apple-m4-pro-with-14-core-cpu-and-20-core-gpu-24gb-memory-512gb",
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
        product_link="https://jbl-russia.ru/product/jbl-charge-4",
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
        product_link="https://www.amazon.com/Canon-Full-Frame-Mirrorless-Lightweight-Smartphone/dp/B0BTTTH5G6?crid=XB9UTR2B5ZA2&dib=eyJ2IjoiMSJ9.m_smke2encA--g4kjseOJbAcjrGpF3srTbwAn8zFSDEpMjcx5dv0osPTTEw4mAh1FI-kLJocIpmIi4irXjfP5pma-eSS9HuIiRKIfPv8Sr-sU0uguGr1mlyTD5haEmi9YbTB6gT92bhEV06L99MfS7I4g-gCqY1oZNBZ0BaVMhYtrcbbPAuCN2EqcP0tMQ6Lbd2oukZwP1vACaMqmtXH4AgcxZnVcC75GF0bHOAjwQg.J7BKhS6yTWWw3KQdwYPYDwibHBxAZJvTckvhZoPChUY&dib_tag=se&keywords=Canon+EOS+R&qid=1731939416&sprefix=macbook+pro+16%2Caps%2C443&sr=8-1",
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
        product_link="Apple Store",
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
        product_link="https://re-store.ru/catalog/MKN93/",
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
        product_link="Dell Store",
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
        product_link="https://www.ozon.ru/product/logitech-klaviatura-besprovodnaya-mx-keys-s-russkaya-raskladka-chernyy-seryy-1343249019/?asb=7bT6GXwIKRKh0ZciV7Zrx42V3W6Ck0hrZqq44SON4GE%253D&asb2=tEbDas2UsUy-pVeFghggZcLCaxIJxCIDoBqaUCrwJWFkEFlji9DGueU69d2QZ_lzQJu5TfG8crCYFuN2GV-QaA&avtc=1&avte=4&avts=1731939500&keywords=%D0%9A%D0%BB%D0%B0%D0%B2%D0%B8%D0%B0%D1%82%D1%83%D1%80%D1%8B+Logitech+MX+KEYS",
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
