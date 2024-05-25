from faker import Faker
from datetime import datetime
import random as rd
import uuid
from typing import Optional
import pydantic

from faux.core.models import (
    User,
    CheckoutEvent,
    VisitEvent,
    VisitEventData,
    CheckoutEventData,
    CART_UPDATE_EVENT,
    AddToCartEvent,
    RemoveFromCartEvent,
    AddToCartEventData,
    RemoveFromCartEventData,
    CHECKOUT_STATUS,
)


# TODO: see if you can access the BROWSER_TYPE values directly from the type object
browsers = ("chrome", "duckduckgo", "firefox", "opera")
qty_min = 1
qty_max = 5

fake = Faker()

# pydantic dump_model has a dump_mode arg
# options can be 'json' or 'python' - json returns dict of json serialiable data


def generate_customer(dump_mode: str = "json") -> dict:
    """
    Generates a fake customer and returns it as a dictionary.

    :param dump_mode: The mode to dump the model. Options are 'json' or 'python'.
    json returns a dictionary that is json-serializable while python will
    return a python dictionary with non-json serializable objects like
    UUID and datetime.
    :return: A dictionary representation of the generated customer.
    """

    user = User(username=fake.user_name(), email=fake.email(), location=fake.city())
    return dump_model(user, dump_mode)


def generate_visit_event(
    customer_id: uuid.UUID, ts: datetime = None, dump_mode: str = "json"
) -> dict:
    """
    Generates a visit event for a given customer.

    :param customer_id: The unique identifier of the customer.
    :param ts: Optional timestamp for the event. If not provided, the current time is used.
    :param dump_mode: The mode to dump the model. Options are 'json' or 'python'.
    :return: A dictionary representation of the generated visit event.
    """
    if ts:
        visit = VisitEvent(
            timestamp=ts,
            customer_id=customer_id,
            event_type="visit",
            event_data=VisitEventData(browser=rd.choice(browsers), timestamp=ts),
        )
    else:
        visit = VisitEvent(
            customer_id=customer_id,
            event_type="visit",
            event_data=VisitEventData(browser=rd.choice(browsers)),
        )
    return dump_model(visit, dump_mode)


def generate_cart_update_event(
    customer_id: uuid.uuid4,
    item_id: uuid.uuid4,
    event_type: CART_UPDATE_EVENT,
    qty: Optional[int] = None,
    dump_mode: str = "json",
) -> dict:
    """
    Generates a visit event for a given customer.

    :param customer_id: The unique identifier of the customer.
    :param ts: Optional timestamp for the event. If not provided, the current time is used.
    :param dump_mode: The mode to dump the model. Options are 'json' or 'python'.
    :return: A dictionary representation of the generated visit event.
    """
    event_data = (
        AddToCartEventData(item_id=item_id, quantity=qty)
        if event_type == "add_to_cart"
        else RemoveFromCartEventData(item_id=item_id)
    )

    event = (
        AddToCartEvent(customer_id=customer_id, event_data=event_data)
        if event_type == "add_to_cart"
        else RemoveFromCartEvent(customer_id=customer_id, event_data=event_data)
    )

    return dump_model(event, dump_mode)


def generate_checkout_event(
    customer_id: uuid.UUID,
    order_id: uuid.UUID,
    status: CHECKOUT_STATUS,
    checked_out_at: datetime,
    dump_mode: str = "json",
) -> dict:
    """
    Generates a checkout event for a given customer.

    :param customer_id: The unique identifier of the customer.
    :param order_id: The unique identifier of the order.
    :param status: The status of the checkout ('success', 'failed', 'cancelled').
    :param checked_out_at: The timestamp when the checkout occurred.
    :param dump_mode: The mode to dump the model. Options are 'json' or 'python'.
    :return: A dictionary representation of the generated checkout event.
    """
    # use the generated orderId to populate a payments table
    checkout = CheckoutEvent(
        customer_id=customer_id,
        event_type="checkout",
        event_data=CheckoutEventData(
            status=status, order_id=order_id, timestamp=checked_out_at
        ),
    )
    return dump_model(checkout, mode=dump_mode)


def dump_model(model: pydantic.BaseModel, mode: str = "json") -> dict:
    """
    Dumps a Pydantic model to a dictionary based on the specified mode.

    :param model: The Pydantic model instance to dump.
    :param mode: The mode of dumping. 'json' for JSON serializable dict,
        'python' for dict with possible non-serializable objects.
    :return: A dictionary representation of the model.
    """
    if mode not in {"json", "python"}:
        raise ValueError(f"Unsupported dump mode: {mode}")

    if mode == "json":
        return model.model_dump(mode="json")
    return model.model_dump()
