from faux.database.base import Base

from sqlalchemy import Column, String, DateTime, Float, JSON
from sqlalchemy.dialects.postgresql import UUID


class User(Base):
    """
    A model representing a user.

    Attributes:
        id (UUID): The unique identifier for the user.
        timestamp (DateTime): The timestamp when the user record was created.
        username (String): The username of the user.
        email (String): The email address of the user.
        location (String): The location of the user.
    """

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True)
    timestamp = Column(DateTime)
    username = Column(String)
    email = Column(String)
    location = Column(String)


class Product(Base):
    """
    A model representing a product.

    Attributes:
        id (UUID): The unique identifier for the product.
        timestamp (DateTime): The timestamp when the product record was created.
        name (String): The name of the product.
        price (Float): The price of the product.
    """

    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True)
    timestamp = Column(DateTime)
    name = Column(String)
    price = Column(Float)


# TODO: rename to Event for consistency.
class Events(Base):
    """
    A model representing an event.

    Attributes:
        id (UUID): The unique identifier for the event.
        timestamp (DateTime): The timestamp when the event occurred.
        customer_id (UUID): The unique identifier of the customer associated with the event.
        event_type (String): The type of event.
        event_data (JSON): The data associated with the event.
    """

    __tablename__ = "events"

    id = Column(UUID(as_uuid=True), primary_key=True)
    timestamp = Column(DateTime)
    customer_id = Column(UUID(as_uuid=True))
    event_type = Column(String)
    event_data = Column(JSON)
