from datetime import datetime
from typing import List, Optional

from Components.StationSector import StationSector
from Events.Event import Event
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
        free_train = self.__is_train_full(environment)

        # Security catch to prevent None reference
        if free_sector is None and not environment.train.is_full():
            raise RuntimeError(
                "We could not find a free sector for passenger, and the train is not full. "
                "Should never have happened.")

        # To stop the passenger from running around the station
        # if the train is full, we return an empty list to prevent
        # the passenger from ending in an endless loop.
        if environment.train.is_full():
            return []

        # Add the passenger to the free sector
        free_sector.add(passenger)

        self.logger.info(
            "Moved passenger from sector {} to sector {}".format(self.sector.sector_index, free_sector.sector_index)
        )
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

        # We loop through the length of the train to find a sector
        for i in range(environment.train.train_car_length):
            left_index = current_index - (i + 1)
            right_index = current_index + (i + 1)

            left_sector = None
            right_sector = None

            if left_index >= 0 and environment.station.sectors[left_index].has_train_car():
                left_sector = environment.station.sectors[left_index]
            if right_index < self.configuration.station_sector_count \
                    and environment.station.sectors[right_index].has_train_car():
                right_sector = environment.station.sectors[right_index]

            # If we could not find a sector to the left and we found one
            # to the right, then we just choose the right
            if left_sector is None and right_sector is not None:
                return right_sector
            # And the other way around, then we choose the left
            elif right_sector is None and left_sector is not None:
                return left_sector
            elif left_sector is not None and right_sector is not None:
                # If the left sector has fewer people than the right,
                # then we choose that. Otherwise, we choose the right.
                if left_sector.amount < right_sector.amount:
                    return left_sector
                else:
                    return right_sector
