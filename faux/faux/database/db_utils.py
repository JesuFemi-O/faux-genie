from sqlalchemy import select, func
from faux.database.db_models import Product, User, Events
from faux.core.models import Product as ProductModel
from faux.database.base import Session, Base, engine
from typing import Any
from pathlib import Path
import json
import logging

logger = logging.getLogger(__name__)


def table_is_empty(session, model) -> bool:
    """
    Checks if a table is empty.

    :param session: The SQLAlchemy session to use for the query.
    :param model: The model class representing the table to check.
    :return: True if the table is empty, False otherwise.
    """
    return session.query(model).count() == 0


def seed_products_table():
    """
    Seeds the products table with initial data from a JSON file.

    If the table is empty, it loads product data from 'config/products.json'
    and inserts it into the table. Logs the process.
    """
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
    """
    Retrieves a specified number of random product IDs from the database.

    :param num_ids: The number of product IDs to retrieve.
    :return: A list of product IDs as strings.
    """
    with Session() as session:
        query = select(Product.id).order_by(func.random()).limit(num_ids)
        result = session.execute(query).scalars().all()
    return [product_id for product_id in result]


def write_to_sink(data: list[dict[str, Any]]) -> None:
    """
    Writes customer and event data to the database.

    :param data: A list of dictionaries containing customer and event data.
    """
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
    """
    Starts the application by initializing the database schema and seeding the products table.

    This function creates all tables defined in the Base metadata and seeds the products table.
    """
    logger.info("Starting DB to initiate data generation")
    Base.metadata.create_all(engine)
    seed_products_table()
