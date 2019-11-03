

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
        Equations taken from:
        https://www.dummies.com/education/science/physics/how-to-calculate-time-and-distance-from-acceleration-and-velocity/
        Train data is taken from: https://da.wikipedia.org/wiki/Litra_SE
        ** The function assumes that we can accelerate to cruise speed, cruise and then retard to 0. **
    Returns:
        The time it takes to travel the distance in seconds
    """
    m_travel_distance = travel_distance * 1000
    ms_cruise_speed = cruise_speed / 0.2777

    acceleration_time = (ms_cruise_speed - 0) / acceleration
    acceleration_distance = 0.5 * acceleration * (acceleration_time ** 2)

    retard_time = (ms_cruise_speed - 0) / retardation
    retard_distance = 0.5 * retardation * (retard_time ** 2)

    cruise_distance = m_travel_distance - (acceleration_distance + retard_distance)
    cruise_time = cruise_distance * ms_cruise_speed

    return acceleration_time + retard_time + cruise_time
