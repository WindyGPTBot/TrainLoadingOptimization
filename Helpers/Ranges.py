from numpy import random


def random_between_range(seed: int, rang: range) -> int:
    """
    Get a random between the provided range object
    Args:
        seed: The seed to be used (usually passed from the configuration object). If None is passed, we use Python's.
        rang: The range object defining the interval
    Returns: An integer i where rang.start <= i < rang.stop
    """
    random.seed(seed)
    if rang.start >= rang.stop:
        return rang.start
    return random.randint(rang.start, rang.stop)


def random_between_percentage(seed: int, rang: range, max_cap: int) -> float:
    """
    Compute a random number under the max_cap within the range percentage.
    It is computed as (random_percentage / 100 * max_cap)
    Args:
        seed: The seed to be used (usually passed from the configuration object). If None is passed, we use Python's.
        rang: The range object between should be values 0 and 100
        max_cap: The maximum number to be returned.
            In the case that the random percentage is 100, then max_cap is returned.
    Returns: The computed random number using the formula above
    """
    return random_between_range(seed, rang) / 100 * max_cap

