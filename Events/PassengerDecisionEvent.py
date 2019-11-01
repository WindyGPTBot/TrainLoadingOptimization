import datetime
from typing import List

from Components.LightStatus import LightStatus
from Components.Passenger import Passenger
from Components.StationSector import StationSector
from Events.Event import Event
from Runtimes import Configuration
from Runtimes.Environment import Environment
from Helpers.Ranges import random_between_range


class PassengerDecisionEvent(Event):
    """
    Event that represents when a passenger on the station must make
    a decision based on the new light status. This event will also
    be responsible for moving the passengers on the station around
    based on their decisions.
    """
    def __init__(self, timestamp: datetime, configuration: Configuration):
        super().__init__(timestamp, configuration)

    def fire(self, environment: Environment) -> List[Event]:
        super().log_event()
        for sector in environment.station.sectors:
            light_status = sector.light.status
            # The passengers stay if they are in a green sector
            if light_status == LightStatus.GREEN:
                self.__handle_green_light(sector, environment)
            elif light_status == LightStatus.YELLOW:
                self.__handle_yellow_light(sector, environment)
            else:
                self.__handle_red_light(sector, environment)
        return {}

    def __handle_green_light(self, sector: StationSector, environment: Environment) -> None:
        """
        This method handles what the passengers in a section with a green light should do
        Args:
            sector: The sector with the green light
            environment: The simulation environment
        """
        return None

    def __handle_yellow_light(self, sector: StationSector, environment: Environment) -> None:
        """
        This method handles what the passengers in a section with a yellow light should do
        Args:
            sector: The sector with the yellow light
            environment: The simulation environment
        """
        current_index = sector.sector_index
        current_amount = sector.amount

        # Get the left and right indexes to this sector
        # We set the initial amount of those to the max allowed sector capacity
        # so that we make sure that we do not move any passengers to those sectors
        # if they are out of bounds or something like that.
        left_index = current_index - 1
        left_amount = self.configuration.station_sector_passenger_max_count + 1
        right_index = current_index + 1
        right_amount = self.configuration.station_sector_passenger_max_count + 1

        # Let us check up on the sector to the left of the current sector
        if left_index >= 0:
            left_sector = environment.station.sectors[left_index]
            # If the left light is green, then we will see if we want to move left
            if left_sector.light.status == LightStatus.GREEN:
                left_amount = left_sector.amount
        # Last, let us check up on the sector to the right
        if right_index <= len(environment.station.sectors) - 1:
            right_sector = environment.station.sectors[right_index]
            # Again, only if the right light is green, we will move
            if right_sector.light.status == LightStatus.GREEN:
                right_amount = right_sector.amount

        # If the sector to the left has fewer passengers than the
        # current sector and fewer than the sector to the right,
        # then we move some passengers to the left sector.
        if current_amount > left_amount < right_amount:
            PassengerDecisionEvent.__move_passengers(current_index, left_index, environment)

        # Otherwise, if the right has the least amount then
        # we move passengers to the right sector instead
        elif current_amount > right_amount < left_amount:
            PassengerDecisionEvent.__move_passengers(current_index, right_index, environment)

    def __handle_red_light(self, sector: StationSector, environment: Environment) -> None:
        """
        This method handles what the passengers in a section with a red light should do
        Args:
            sector: The sector with the red light
            environment: The simulation environment
        """
        pass

    @staticmethod
    def __move_passengers(from_index: int,
                          to_index: int,
                          environment: Environment) -> None:
        """
        Helper function that move the passengers from on sector to another.
        Will randomly choose a number (of passengers) between 0% and 100% of the from_index sector
        that will be moved to the to_index sector.
        Args:
            from_index: The sector index where we will move passengers from
            to_index: The sector index where we will move passengers to
            environment: The simulation environment
        """
        # A random amount between 0 and 100% of the passengers in the from sector
        amount = random_between_range(range(0, environment.station.sectors[from_index].amount))
        # Remove the passengers from the sector
        passengers = environment.station.sectors[from_index].remove(amount)
        # Move them to the new sector
        environment.station.sectors[to_index].add(passengers)
