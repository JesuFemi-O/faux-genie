import random
from datetime import datetime
from typing import Any, Optional, Union
from faux.core import faux_utils
from faux.simulator.sim_helpers import (
    _to_timestamp,
    _to_uuid,
    generate_timestamps,
    _generate_new_timestamp,
    add_random_minutes,
)
from database.db_utils import get_product_ids, write_to_sink
import uuid


def generate_new_users(num_users: int = 100) -> dict[str, Any]:
    return [faux_utils.generate_customer() for i in range(num_users)]


# TODO: create a custom type for common union types in project. e.g. T_UUID_STR = str | uuid
# types i have in mind: AnyDict, T_UUID_STR, T_UUID_DATETIME
def generate_visit(
    customer_id: Union[str, uuid.UUID],
    timestamp_str: Optional[Union[str, uuid.UUID]] = None,
) -> dict[str, Any]:
    if timestamp_str:
        timestamp = _to_timestamp(timestamp_str)
    else:
        timestamp = None
    return faux_utils.generate_visit_event(
        customer_id=_to_uuid(customer_id), ts=timestamp
    )


def generate_historic_visits(
    customer_id: Union[str, uuid.UUID], base_ts: datetime
) -> dict[str, Any]:
    # TODO: move hardcoded values into config variables
    if random.choice([0, 1]) > 0:
        ts_array = generate_timestamps(base_ts)
        return [
            generate_visit(customer_id=customer_id, timestamp_str=visit_date)
            for visit_date in ts_array
        ]
    return []


def generate_add_to_cart(
    customer_id: Union[str, uuid.UUID], item_id: Union[str, uuid.UUID]
) -> dict[str, Any]:
    # TODO: move hardcoded values into config variables
    return faux_utils.generate_cart_update_event(
        customer_id=_to_uuid(customer_id),
        item_id=_to_uuid(item_id),
        event_type="add_to_cart",
        qty=random.randint(1, 5),
    )


def generate_remove_from_cart(
    customer_id: Union[str, uuid.UUID], item_id: Union[str, uuid.UUID]
) -> dict[str, Any]:
    return faux_utils.generate_cart_update_event(
        customer_id=_to_uuid(customer_id),
        item_id=_to_uuid(item_id),
        event_type="remove_from_cart",
    )


def generate_checkout(
    customer_id: Union[str, uuid.UUID],
    order_id: Union[str, uuid.UUID],
    status: str,
    checked_out_at: Union[str, datetime],
) -> dict[str, Any]:
    return faux_utils.generate_checkout_event(
        customer_id=_to_uuid(customer_id),
        order_id=_to_uuid(order_id),
        checked_out_at=checked_out_at,
        status=status,
    )


def generate_customer_data():
    # Generate visit event
    # the simulation here should let me generate 0 - 5 previous visits for the customer
    # generate a timestamp
    # randomly go back up to a time stamp up to 10 days in the past
    # not all customers must have historic visits

    # in the future I should pick between new or existing customer
    customer = generate_new_users(num_users=1)[0]
    customer_id = customer["id"]
    customer_data = {"customer": customer}

    # a potential issue here is that hsitoric events can go as far back as 10 days before the base timestamp
    # customers created_at has to always be at least 11 days from current timestamp
    customer_data["events"] = generate_historic_visits(
        customer_id=customer_id, base_ts=_generate_new_timestamp(iso=False)
    )

    # Simulate sequential events
    for _ in range(random.randint(1, 5)):  # Random number of visits
        visit_event = generate_visit(customer_id=customer_id)
        customer_data["events"].append(visit_event)

    # need a function to pick K random products from the product table
    num_picks = random.randint(1, 12)
    item_ids = get_product_ids(num_ids=num_picks)
    for item_id in item_ids:
        customer_data["events"].append(
            generate_add_to_cart(
                customer_id=_to_uuid(customer_id), item_id=_to_uuid(item_id)
            )
        )

        if random.choice(
            [True, False]
        ):  # Simulate remove_from_cart only if add_to_cart occurred
            # print("removing from cart...")
            customer_data["events"].append(
                generate_remove_from_cart(
                    customer_id=_to_uuid(customer_id), item_id=_to_uuid(item_id)
                )
            )

    add_to_cart_count = sum(
        1 for event in customer_data["events"] if event["event_type"] == "add_to_cart"
    )
    remove_from_cart_count = sum(
        1
        for event in customer_data["events"]
        if event["event_type"] == "remove_from_cart"
    )

    line_items = None
    checked_out_at = None
    order_id = None
    status = None

    # Simulate checkout event after add_to_cart events - you can't checkout with empty cart
    if add_to_cart_count > remove_from_cart_count:
        checked_out_at = add_random_minutes(_generate_new_timestamp(iso=False))

        # An order is only created at the point of checkout
        order_id = uuid.uuid4()
        status = random.choice(["success", "failed", "cancelled"])

        customer_data["events"].append(
            generate_checkout(
                customer_id=customer_id,
                order_id=order_id,
                status=status,
                checked_out_at=checked_out_at,
            )
        )

        abandon_cart = random.choice([True, False])

        if not abandon_cart:
            line_items = []

            for event in customer_data["events"]:
                # Still unsure about actually keeping this in the db
                if event["event_type"] == "add_to_cart":
                    line_items.append(
                        {
                            "item_id": event["event_data"]["item_id"],
                            "quantity": event["event_data"]["quantity"],
                            "order_id": order_id,
                        }
                    )
        else:
            # Remove the checkout event to simulate an abandoned cart
            customer_data["events"] = [
                event
                for event in customer_data["events"]
                if event["event_type"] != "checkout"
            ]
    # the intentional error in this code that the line items array doesn't consider items that were removed from the cart
    return customer_data


def create_simulation(n=1000):
    # TODO: make the default value of n a CONSTANT stored in a config
    events_data = []
    for _ in range(n):
        data = generate_customer_data()
        events_data.append(data)
    return events_data
