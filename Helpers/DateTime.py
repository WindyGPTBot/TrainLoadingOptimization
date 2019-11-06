from datetime import timedelta, datetime


def add_seconds(dt: datetime, seconds) -> datetime:
    """
    Add seconds to the provided datetime
    Args:
        dt: The datetime to add seconds to
        seconds: The amount of seconds to add
    Returns:
        The dt with the added seconds
    """
    return dt + timedelta(seconds=seconds)
