from datetime import datetime
from typing import List, Optional

from Components.StationSector import StationSector
from Events.Event import Event
from Events.PrepareTrainEvent import PrepareTrainEvent
from Helpers.Distances import sector_distance
from Helpers.Speed import compute_walking_speed
from Runtimes.Configuration import Configuration
from Runtimes.Environment import Environment


class MovePassengerEvent(Event):
    """
    Event responsible for moving a single passenger around the station platform.
    **Assumes that the train is parked.**
    """

    def __init__(self, sector: StationSector, amount: int, timestamp: datetime, configuration: Configuration):
        """
        Initialize a new Move Passenger Event
        Args:
            sector: The sector the passenger is moving from
            timestamp: The event timestamp
            configuration: The simulation configuration
        """
        self.sector = sector
        self.amount = amount
        super().__init__(timestamp, configuration)

    def fire(self, environment: Environment) -> List[Event]:

        if self.amount == 0:
            self.logger.warning("Amount was zero for sector {}.".format(self.sector.sector_index))
            return []

        # Get the nearest sector with least people
        free_sector = self.__get_nearby_free_sector(environment)

        # Security catch to prevent None reference
        if free_sector is None and not environment.train.is_full():
            raise RuntimeError(
                "We could not find a free sector for passenger, and the train is not full. "
                "Should never have happened.")

        # Compute the walking distance
        walking_distance = sector_distance(self.sector, free_sector)
        # Now, remove the passenger from the current sector
        removed_passengers = self.sector.remove(self.amount)
        # For ease of use later, let's record how many we removed
        amount_removed = len(removed_passengers)
        try:
            # Compute how long it takes to walk that distance
            speed = compute_walking_speed(removed_passengers[0], walking_distance)
            # Now perform the action
            self.do_action(speed, "Moved {} passengers from sector {} to {}".format(amount_removed,
                                                                                    self.sector.sector_index,
                                                                                    free_sector.sector_index))
        except IndexError:
            self.logger.warning("We removed zero passengers during move in sector {} with {} passengers".format(
                self.sector.sector_index, self.sector.amount))
        # Actually move the passengers
        free_sector.add(removed_passengers)

        from Events.LoadPassengerEvent import LoadPassengerEvent
        return [LoadPassengerEvent(free_sector, amount_removed, self.timestamp, self.configuration)]

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
