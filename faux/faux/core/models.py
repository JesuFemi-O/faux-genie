from pydantic import BaseModel, Field, EmailStr, UUID4
from datetime import datetime
from typing import Literal
import uuid


EVENT_TYPE = Literal["visit", "add_to_cart", "remove_from_cart", "checkout"]
CART_UPDATE_EVENT = Literal["add_to_cart", "remove_from_cart"]
CHECKOUT_STATUS = Literal["success", "failed", "cancelled"]
BROWSER_TYPE = Literal["chrome", "duckduckgo", "firefox", "opera"]


class CustomBase(BaseModel):
    """
    A base model with default id and timestamp fields.

    Attributes:
        id (UUID4): The unique identifier for the model.
        timestamp (datetime): The timestamp when the model instance was created.
    """

    id: UUID4 = Field(default_factory=uuid.uuid4)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class User(CustomBase):
    """
    A model representing a user/customer.

    Attributes:
        username (str): The username of the user.
        email (EmailStr): The email address of the user.
        location (str): The location of the user.
    """

    username: str
    email: EmailStr
    location: str


class Product(CustomBase):
    """
    A model representing a product.

    Attributes:
        name (str): The name of the product.
        price (float): The price of the product.
    """

    name: str
    price: float


class Event(CustomBase):
    """
    A model representing an event.
    The events are common events that occur when
    a customer visits an e-commerce website. The event model will
    serve as a base model for the different types of events.

    Attributes:
        customer_id (UUID4): The unique identifier of the customer associated with the event.
        event_type (EVENT_TYPE): The type of event.
    """

    customer_id: UUID4
    event_type: EVENT_TYPE


class CartItemEventData(BaseModel):
    """
    A model representing the data for a cart item event.

    Attributes:
        item_id (UUID4): The unique identifier of the cart item.
        timestamp (datetime): The timestamp when the event occurred.
    """

    item_id: UUID4
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class CheckoutEventData(BaseModel):
    """
    A model representing the data for a checkout event.

    Attributes:
        status (CHECKOUT_STATUS): The status of the checkout.
        order_id (UUID4): The unique identifier of the order.
        timestamp (datetime): The timestamp when the checkout occurred.
    """

    status: CHECKOUT_STATUS
    order_id: UUID4
    timestamp: datetime


class RemoveFromCartEventData(CartItemEventData):
    """
    A model representing the data for a remove-from-cart event.
    This model maps 1:1 to CartItemEventData but makes it easy
    for us to extend remove from cart event data if the need
    arises in the future.
    """

    pass


class AddToCartEventData(CartItemEventData):
    """
    A model representing the data for an add-to-cart event.

    Attributes:
        quantity (int): The quantity of the item added to the cart.
    """

    quantity: int


class VisitEventData(BaseModel):
    """
    A model representing the data for a visit event.

    Attributes:
        browser (BROWSER_TYPE): The type of browser used during the visit.
        timestamp (datetime): The timestamp when the visit occurred.
    """

    browser: BROWSER_TYPE
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# TODO: remove model!
class CartEvent(Event):
    event_data: CartItemEventData


class AddToCartEvent(Event):
    """
    A model representing an add-to-cart event.

    Attributes:
        event_type (CART_UPDATE_EVENT): The type of cart update event.
        event_data (AddToCartEventData): The data associated with the add-to-cart event.
    """

    event_type: CART_UPDATE_EVENT = "add_to_cart"
    event_data: AddToCartEventData


class RemoveFromCartEvent(Event):
    """
    A model representing a remove-from-cart event.

    Attributes:
        event_type (CART_UPDATE_EVENT): The type of cart update event.
        event_data (CartItemEventData): The data associated with the remove-from-cart event.
    """

    event_type: CART_UPDATE_EVENT = "remove_from_cart"
    event_data: CartItemEventData


class CheckoutEvent(Event):
    """
    A model representing a checkout event.

    Attributes:
        event_type (EVENT_TYPE): The type of event.
        event_data (CheckoutEventData): The data associated with the checkout event.
    """

    event_type: EVENT_TYPE = "checkout"
    event_data: CheckoutEventData


class VisitEvent(Event):
    """
    A model representing a visit event.

    Attributes:
        event_type (EVENT_TYPE): The type of event.
        event_data (VisitEventData): The data associated with the visit event.
    """

    event_type: EVENT_TYPE = "visit"
    event_data: VisitEventData
