from datetime import datetime
from typing import List, Optional

from Components.StationSector import StationSector
from Events.Event import Event
from Helpers.Speed import compute_walking_speed
from Runtimes.Configuration import Configuration
from Runtimes.Environment import Environment


class MovePassengerEvent(Event):
    """
    Event responsible for moving a single passenger around the station platform.
    **Assumes that the train is parked.**
    """

    def __init__(self, sector: StationSector, timestamp: datetime, configuration: Configuration):
        """
        Initialize a new Move Passenger Event
        Args:
            sector: The sector the passenger is moving from
            timestamp: The event timestamp
            configuration: The simulation configuration
        """
        self.sector = sector
        super().__init__(timestamp, configuration)

    def fire(self, environment: Environment) -> List[Event]:

        # Remove the passenger from the sector
        passenger = self.sector.remove(1)

        # Get the nearest sector with least people
        free_sector = self.__get_nearby_free_sector(environment)

        # Security catch to prevent None reference
        if free_sector is None and not environment.train.is_full():
            raise RuntimeError(
                "We could not find a free sector for passenger, and the train is not full. "
                "Should never have happened.")

        # To stop the passenger from running around the station
        # if the train is full, we return an empty list to prevent
        # the passenger from ending in an endless loop.
        if environment.train.is_full():
            self.logger.warning("The train is full for passenger {}".format(passenger[0].id))
            return []

        # Add the passenger to the free sector
        free_sector.add(passenger)

        distance = abs(self.sector.sector_index - free_sector.sector_index)
        speed = compute_walking_speed(passenger[0], distance)
        message = "Moved passenger from sector {} to sector {}".format(self.sector.sector_index, free_sector.sector_index)
        self.do_action(speed, message)
        # We return the load event so that passenger can get loaded
        from Events.LoadPassengerEvent import LoadPassengerEvent  # Inline/local import to prevent reference error
        return [LoadPassengerEvent(free_sector, self.timestamp, self.configuration)]

    def __is_train_full(self, environment: Environment) -> bool:
        """
        Check whether the train is full or not
        """
        train_sets = environment.train.train_sets
        for t_set in train_sets:
            # Check if any of the cars is not full
            if any([c.is_full() for c in t_set.cars]):
                return True
        return False

    def __get_nearby_free_sector(self, environment: Environment) -> Optional[StationSector]:
        """
        Get the nearest sector with least people.
        The search goes both right and left and chooses the one with the least people in.
        Args:
            environment: The simulation environment
        Returns:
            The nearest StationSector with the least people.
            Return None in cases where we could not find a station sector. Should never be the case.
        """
        current_index = self.sector.sector_index
        left_index = current_index - 1
        right_index = current_index + 1

        least_sector = None

        for i in range(self.configuration.station_sector_count):
            if least_sector is not None:
                break
            left_sector = None
            right_sector = None
            if left_index >= 0:
                left_sector = environment.station.sectors[left_index]
            if right_index < self.configuration.station_sector_count:
                right_sector = environment.station.sectors[right_index]

            if left_sector is not None and right_sector is not None:
                least_sector = left_sector if left_sector.amount < right_sector.amount else right_sector
            elif left_sector is not None:
                least_sector = left_sector
            elif right_sector is not None:
                least_sector = right_sector
            left_index += 1
            right_index += 1
        return least_sector
