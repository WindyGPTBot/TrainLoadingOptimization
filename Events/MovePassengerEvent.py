from datetime import datetime
from typing import List, Optional
from Helpers.Acceleration import compute_driving_time
from Components.Passenger import Passenger
from Components.StationSector import StationSector
from Events.Event import Event
from Events.LoadPassengerEvent import LoadPassengerEvent
from Runtimes import RunTime
from Runtimes.Configuration import Configuration
from Runtimes.Environment import Environment


class MovePassengerEvent(Event):
    """
    Event responsible for moving a single passenger around the station platform.
    **Should only be used when the train is parked.**
    """
    def __init__(self, sector: StationSector, timestamp: datetime, configuration: Configuration):
        super().__init__(timestamp, configuration)
        self.sector = sector

    def __fire(self, environment: Environment) -> List[Event]:
        # Remove the passenger from the sector
        passenger = environment.station.sectors[self.sector.sector_index].remove(1)
        # Get the nearest sector with least people
        free_sector = self.__get_nearby_free_sector(environment)

        if free_sector is None:
            raise RuntimeError("We could not find a free sector for the passenger. Should never have happened.")

        # Add the passenger to the free sector
        free_sector.add(passenger)

        # We return the load event so that passenger can get loaded
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
        current_index = self.sector.sector_index
        left_index = current_index - 1
        right_index = current_index + 1

        # We loop through the length of the train to find a sector
        for i in range(environment.train.train_car_length):
            left_sector = None
            right_sector = None
            if left_index > 0:
                try:
                    environment.get_train_car_at_sector(left_index)
                    left_sector = environment.station.sectors[left_index]
                except IndexError:
                    self.logger.debug("There was no train at left sector {}".format(left_index))
            if right_index < self.configuration.station_sector_count:
                try:
                    environment.get_train_car_at_sector(right_index)
                    right_sector = environment.station.sectors[right_index]
                except IndexError:
                    self.logger.debug("There was no train at right sector {}".format(right_index))

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
        # Good practice is to always return something.
        # This should never happen, and must be caught.
        return None
