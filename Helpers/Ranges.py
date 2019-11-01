from numpy.random import randint

def random_between_range(rang: range) -> int:
    """
    Get a random between the provided range object
    Args:
        rang: The range object defining the interval
    Returns: An integer i where rang.start <= i < rang.stop
    """
    return randint(rang.start, rang.stop)


def random_between_percentage(rang: range, max_cap: int) -> float:
    """
    Compute a random number under the max_cap within the range percentage.
    It is computed as (random_percentage / 100 * max_cap)
    Args:
        rang: The range object between should be values 0 and 100
        max_cap: The maximum number to be returned.
            In the case that the random percentage is 100, then max_cap is returned.
    Returns: The computed random number using the formula above
    """
    return random_between_range(rang) / 100 * max_cap

