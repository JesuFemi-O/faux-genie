from pydantic import BaseModel, Field, EmailStr, UUID4
from datetime import datetime
from typing import Literal
import uuid


EVENT_TYPE = Literal["visit", "add_to_cart", "remove_from_cart", "checkout"]
CART_UPDATE_EVENT = Literal["add_to_cart", "remove_from_cart"]
CHECKOUT_STATUS = Literal["success", "failed", "cancelled"]
BROWSER_TYPE = Literal["chrome", "duckduckgo", "firefox", "opera"]


class CustomBase(BaseModel):
    id: UUID4 = Field(default_factory=uuid.uuid4)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class User(CustomBase):
    username: str
    email: EmailStr
    location: str


class Product(CustomBase):
    name: str
    price: float


class Event(CustomBase):
    customer_id: UUID4
    event_type: EVENT_TYPE


class CartItemEventData(BaseModel):
    item_id: UUID4
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class CheckoutEventData(BaseModel):
    status: CHECKOUT_STATUS
    order_id: UUID4
    timestamp: datetime


class RemoveFromCartEventData(CartItemEventData):
    pass


class AddToCartEventData(CartItemEventData):
    quantity: int


class VisitEventData(BaseModel):
    browser: BROWSER_TYPE
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# TODO: remove model!
class CartEvent(Event):
    event_data: CartItemEventData


class AddToCartEvent(Event):
    event_type: CART_UPDATE_EVENT = "add_to_cart"
    event_data: AddToCartEventData


class RemoveFromCartEvent(Event):
    event_type: CART_UPDATE_EVENT = "remove_from_cart"
    event_data: CartItemEventData


class CheckoutEvent(Event):
    event_type: EVENT_TYPE = "checkout"
    event_data: CheckoutEventData


class VisitEvent(Event):
    event_type: EVENT_TYPE = "visit"
    event_data: VisitEventData
