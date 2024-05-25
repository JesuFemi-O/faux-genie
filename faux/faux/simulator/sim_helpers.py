import random
from datetime import datetime, timedelta
from typing import Optional, Union
import uuid


def generate_timestamps(
    base_timestamp: datetime, iso: bool = True
) -> list[Union[datetime, str]]:
    # Define the maximum number of timestamps to generate (between 1 and 5)
    num_timestamps = random.randint(1, 5)

    # Define the maximum number of days, hours, minutes, and seconds to go back
    max_days_before = 10
    max_hours_before = 23
    max_minutes_before = 59
    max_seconds_before = 59

    # Initialize an empty list to store the generated timestamps
    timestamps = []

    # Generate random timestamps
    for _ in range(num_timestamps):
        # Generate random components for days, hours, minutes, and seconds
        days_before = random.randint(1, max_days_before)
        hours_before = random.randint(0, max_hours_before)
        minutes_before = random.randint(0, max_minutes_before)
        seconds_before = random.randint(0, max_seconds_before)
        microseconds_before = random.randint(0, 999999)

        # Calculate the new timestamp
        new_timestamp = base_timestamp - timedelta(
            days=days_before,
            hours=hours_before,
            minutes=minutes_before,
            seconds=seconds_before,
            microseconds=microseconds_before,
        )

        # Convert the timestamp to a string and append it to the list
        if iso:
            new_timestamp = new_timestamp.isoformat()
        timestamps.append(new_timestamp)

    return timestamps


def add_random_minutes(timestamp, iso=True):
    # Generate a random number of minutes to add (between 3 and 17)
    minutes_to_add = random.randint(3, 17)

    # Create a timedelta object with the random duration
    duration = timedelta(minutes=minutes_to_add)

    # Add the duration to the input timestamp
    new_timestamp = timestamp + duration

    if iso:
        new_timestamp = new_timestamp.isoformat()

    return new_timestamp


def _to_uuid(uuid_str: str) -> uuid.UUID:
    if isinstance(uuid_str, uuid.UUID):
        return uuid_str
    return uuid.UUID(uuid_str)


def _to_timestamp(timestamp_str: str, format: Optional[str] = None) -> datetime:
    if isinstance(timestamp_str, datetime):
        return timestamp_str
    elif format is not None:
        # Use the provided format
        return datetime.strptime(timestamp_str, format)
    else:
        # Assume ISO 8601 format
        return datetime.fromisoformat(timestamp_str)


def _generate_new_timestamp(iso=True):
    if iso:
        return datetime.now().isoformat()
    return datetime.now()
