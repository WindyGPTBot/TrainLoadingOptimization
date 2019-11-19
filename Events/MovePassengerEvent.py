from datetime import datetime
from typing import List, Optional

from Components.StationSector import StationSector
from Events.Event import Event
from Helpers.Distances import sector_distance
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
            self.logger.warning("The train is full for passenger")
            return []
        if self.sector.empty():
            self.logger.warning("The sector is empty")
            return []
        # Remove the passenger from the sector
        passenger = self.sector.remove(1)

        # Add the passenger to the free sector
        free_sector.add(passenger)

        distance = abs(self.sector.sector_index - free_sector.sector_index)
        speed = compute_walking_speed(passenger[0], distance)
        message = "Moved passenger from sector {} to sector {}".format(self.sector.sector_index,
                                                                       free_sector.sector_index)
        self.do_action(speed, message)
        # We return the load event so that passenger can get loaded
        from Events.LoadPassengerEvent import LoadPassengerEvent  # Inline/local import to prevent reference error
        return [LoadPassengerEvent(free_sector, free_sector.amount, self.timestamp, self.configuration)]

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
        least_sector = None
        least_distance = self.configuration.station_sector_count
        for sector in environment.station.sectors:
            if sector.has_train_car() and not sector.train_car.is_full():
                dist = sector_distance(self.sector, sector)
                if dist < least_distance and dist != 0:
                    if dist == least_distance:
                        least_sector = least_sector if least_sector.amount <= sector.amount else sector
                    else:
                        least_sector = sector
                        least_distance = dist
        return least_sector
