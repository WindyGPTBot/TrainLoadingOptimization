from Components.StationSector import StationSector


def sector_distance(first: StationSector, second: StationSector) -> int:
    """
    Compute the distance between two sectors
    Args:
        first: The first sector
        second: The second sector

    Returns:
        The distance between first and second sector
    """
    if first is None or second is None:
        raise TypeError("Sectors must not be None")
    return abs(first.sector_index - second.sector_index)
