from datetime import datetime
import asyncio
import logging
from logging import config as lc
import os
import sys
import csv

sys.path.append(os.path.join(sys.path[0], ".."))
sys.path.append(os.path.join(sys.path[0], "../api"))

from api.config import settings
from api.repository import ProductRepo
from api.schemas import SPagination, SProductAdd, SSort


lc.dictConfig(settings.logging_config)
logger = logging.getLogger("tests.fill_empty_db")


def read_product_from_csv(csv_path: str) -> list[SProductAdd]:
    products = []
    with open(csv_path, mode="r") as f:
        for raw_dict in csv.DictReader(f):
            clear_dict = {}
            for key in raw_dict:
                if raw_dict[key] == "":
                    pass
                elif key == "price":
                    clear_dict[key] = float(raw_dict[key])
                elif key == "is_purchased":
                    clear_dict[key] = raw_dict[key] == "True"
                elif key == "buy_date":
                    clear_dict[key] = datetime.strptime(
                        raw_dict[key], "%Y-%m-%d"
                    ).date()
                elif key == ["guarantee", "priority"]:
                    clear_dict[key] = int(raw_dict[key])
                else:
                    clear_dict[key] = raw_dict[key]

            products.append(SProductAdd.model_validate(clear_dict))
    return products


async def main():
    responce = await ProductRepo.get_list(SPagination(), SSort())

    logger.info(f"DB total_count: {responce.total_count}")

    if responce.total_count == 0:
        products = read_product_from_csv("./example_droducts.csv")

        logger.info(f"Filling the database with {len(products)} records.")
        for product in products:
            responce = await ProductRepo.add_one(product)
            logger.info(responce)

        logger.info("Filling is complete")


if __name__ == "__main__":
    asyncio.run(main())
