

def compute_driving_time(
        travel_distance: float,
        cruise_speed: float = 90,
        acceleration: float = 1.3,
        retardation: float = 1.2,
) -> float:
    """
    Calculate the time it takes for the train to drive a certain distance
    Args:
        travel_distance: The travel distance in kilometers
        cruise_speed: The cruise speed in kilometers per hour
        acceleration: The acceleration in m/s^2
        retardation: The deceleration in m/s^2
    Notes
        **The function assumes that we can accelerate to cruise speed, cruise and then retard to 0.**
        Equations taken from:
        https://www.dummies.com/education/science/physics/how-to-calculate-time-and-distance-from-acceleration-and-velocity/
        Train data is taken from: https://da.wikipedia.org/wiki/Litra_SE
    Returns:
        The time it takes to travel the distance in seconds
    """
    # Convert the given distance from kilometers to meters
    m_travel_distance = travel_distance * 1000
    # Convert the cruise speed from km/h to m/s
    ms_cruise_speed = cruise_speed / 0.2777

    # First, we must find out how long it takes to accelerate
    # to cruise speed, and how much distance it requires.
    acceleration_time = (ms_cruise_speed - 0) / acceleration
    acceleration_distance = 0.5 * acceleration * (acceleration_time ** 2)

    # Secondly, we must find out how long it takes to decelerate
    # from cruise speed to 0, and how much distance it requires.
    retard_time = (ms_cruise_speed - 0) / retardation
    retard_distance = 0.5 * retardation * (retard_time ** 2)

    # Last, we must find out how long it takes to drive the last cruise distance
    cruise_distance = m_travel_distance - (acceleration_distance + retard_distance)
    cruise_time = ms_cruise_speed / cruise_distance

    return acceleration_time + retard_time + cruise_time
