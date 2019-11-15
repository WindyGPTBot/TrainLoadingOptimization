from Components.Passenger import Passenger


def compute_loading_speed(passenger: Passenger, amount: int) -> float:
    """
    Compute the time in seconds to load the provided passenger
    Args:
        passenger: The passenger who wants to load
        amount: The amount waiting to load
    Returns:
        Seconds it takes to load passenger
    """
    return passenger.loading_time * passenger.size


def compute_walking_speed(passenger: Passenger, distance: int) -> float:
    """
    Compute the time it takes to walk the amount of sectors
    Args:
        passenger: The passenger who wants to walk
        distance: The distance to walk
    Returns:
        The time it takes to walk the distance in seconds
    """
    return passenger.speed * distance
