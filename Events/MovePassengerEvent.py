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
        super().__init__(timestamp, configuration)
        self.sector = sector

    def fire(self, environment: Environment) -> List[Event]:
        # Remove the passenger from the sector
        from_sector = environment.station.sectors[self.sector.sector_index]
        passenger = from_sector.remove(1)
        # Get the nearest sector with least people
        free_sector = self.__get_nearby_free_sector(environment)
        # Security catch to prevent None reference
        if free_sector is None:
            raise RuntimeError("We could not find a free sector for the passenger. Should never have happened.")
        # Add the passenger to the free sector
        free_sector.add(passenger)

        self.logger.info(
            "Moved passenger from sector {} to sector {}".format(from_sector.sector_index, free_sector.sector_index)
        )
        # We return the load event so that passenger can get loaded
        from Events.LoadPassengerEvent import LoadPassengerEvent  # Inline/local import to prevent reference error
        return [LoadPassengerEvent(self.timestamp, self.configuration)]

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
        # We loop through the length of the train to find a sector
        for i in range(environment.train.train_car_length):
            current_index = self.sector.sector_index
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
