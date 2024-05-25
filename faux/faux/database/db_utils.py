from sqlalchemy import select, func
from faux.database.db_models import Product, User, Events
from faux.core.models import Product as ProductModel
from faux.database.base import Session, Base, engine
from typing import Any
from pathlib import Path
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def table_is_empty(session, model) -> bool:
    return session.query(model).count() == 0


def seed_products_table():
    with Session() as session:
        if table_is_empty(session, Product):
            logger.info("Setting up seed data...")
            project_root = Path(__file__).resolve().parents[1]
            product_file_path = project_root / "config/products.json"

            with open(product_file_path, "r") as f:
                products = json.loads(f.read())

            for product in products:
                product_data = ProductModel(
                    name=product["name"], price=product["price"]
                ).model_dump(mode="json")
                product_obj = Product(**product_data)
                session.add(product_obj)

            session.commit()
            logger.info("Seed process completed successfully...")
        else:
            logger.info("Table has already been loaded with products data!")


def get_product_ids(num_ids: int) -> list[str]:
    with Session() as session:
        query = select(Product.id).order_by(func.random()).limit(num_ids)
        result = session.execute(query).scalars().all()
    return [product_id for product_id in result]


def write_to_sink(data: list[dict[str, Any]]) -> None:
    logger.info(f"Writing {len(data)} records to DB")
    users = [User(**customer_data["customer"]) for customer_data in data]
    events = [
        Events(**customer_event)
        for customer_data in data
        for customer_event in customer_data["events"]
    ]

    with Session() as session:
        session.add_all(users)
        session.add_all(events)
        session.commit()
    logger.info("Records written successfully")


def start_application():
    logger.info("Starting DB to initiate data generation")
    Base.metadata.create_all(engine)
    seed_products_table()
