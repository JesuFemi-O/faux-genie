from faux.database.base import Base

from sqlalchemy import Column, String, DateTime, Float, JSON
from sqlalchemy.dialects.postgresql import UUID


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True)
    timestamp = Column(DateTime)
    username = Column(String)
    email = Column(String)
    location = Column(String)


class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True)
    timestamp = Column(DateTime)
    name = Column(String)
    price = Column(Float)


class Events(Base):
    __tablename__ = "events"

    id = Column(UUID(as_uuid=True), primary_key=True)
    timestamp = Column(DateTime)
    customer_id = Column(UUID(as_uuid=True))
    event_type = Column(String)
    event_data = Column(JSON)
