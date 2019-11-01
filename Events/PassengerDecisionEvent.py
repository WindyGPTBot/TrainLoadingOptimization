import datetime
from typing import List, Dict, Union

from Components.LightStatus import LightStatus
from Components.Passenger import Passenger
from Components.StationSector import StationSector
from Events.Event import Event
from Helpers.Ranges import random_between_range
from Runtimes import Configuration
from Runtimes.Environment import Environment


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
        self.log_event()
        for sector in environment.station.sectors:
            light_status = sector.light.status
            # The passengers stay if they are in a green sector
            if light_status == LightStatus.GREEN:
                self.__handle_green_light(sector, environment)
            elif light_status == LightStatus.YELLOW:
                self.__handle_yellow_light(sector, environment)
            else:
                self.__handle_red_light(sector, environment)
        return []

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
        Notes
            @TODO: This should probably be based on how much time the passengers have to move
        """
        # We initialize a dictionary with the keys corresponding to the distances
        # from this sector up to the max walking distance that a passenger can be initialized with.
        # It will be filled with lists of sectors that have been lit with green lights.
        green_sectors = self.__create_distance_dictionary(environment, sector)

        # Now that we have the dictionary with the station sectors sorted by
        # the distance from this sector, we can start to move passengers around
        # the platform based on how much time and distance to the other sectors.
        for passenger in sector.passengers:
            # If the passenger is not willing to walk any distance or the passenger
            # is not compliant, then we just continue to be efficient.
            if passenger.max_walk == 0 or not passenger.is_compliant():
                continue

            # Now the passenger will make a decision for which sector to move.
            chosen_sector = self.__choose_sector(green_sectors, passenger)

            # If we get None as the chosen sector, it means that we could not find
            # station sector for the current passenger and we therefore don't move him.
            # If we do find a station sector, then we pop that passenger from the current
            # sector and add him to the chosen sector.
            if chosen_sector is not None:
                # Remove the passenger from the current sector
                environment.station.sectors[sector.sector_index].remove_passenger(passenger)
                # Add the passenger to the chosen sector
                environment.station.sectors[chosen_sector.sector_index].add(passenger)

    def __choose_sector(self, sectors: Dict[int, List[StationSector]],
                        passenger: Passenger) -> Union[StationSector, None]:
        """
        The given passenger will choose a sector that he have the time and
        wants to walk to.
        Args:
            sectors: The station sectors that we can move to.
            passenger: The passenger that is taking the decision.
        Returns:
            StationSector object that the passenger should move to, or
            None if no green station sector was in range.
        """
        # The sector to return
        sector = None

        # Now we will loop through all distances, to
        # figure out where the passenger wants to go.
        for distance in sectors.keys():
            # Let us not worry about the stations out of reach
            # for the passenger.
            # @TODO: This is where the time check should be, so that we
            #   only move passengers that have the time to move that distance.
            if distance > passenger.max_walk:
                break
            # Let us loop through all the station sectors at the current distance
            # and see if we can find a more suitable sector to move the passenger to
            for sector_at_distance in sectors[distance]:
                # If this is the first sector, then this
                # will be the first selected sector
                if sector is None:
                    sector = sector_at_distance
                # If the amount of passengers at the current selected station sector
                # is lower than the amount of passengers at the current loop station sector,
                # then we set the current station sector to the loop station sector.
                elif len(sector.passengers) > len(sector_at_distance.passengers):
                    sector = sector_at_distance

        return sector

    def __create_distance_dictionary(self, environment: Environment,
                                     current_sector: StationSector) -> Dict[int, List[StationSector]]:
        """
        Private method that creates a dictionary with distances as keys that maps to StationSectors at that distance.
        Args:
            environment: The simulation environment
            current_sector: The current sector
        Returns:
            A dictionary that maps distances (int) to a list of station sectors which are that distance from the
            current sector.
        """
        # The max distance a passenger can be spawned with
        passenger_max_walk_distance = self.configuration.passenger_max_walk_range.stop
        # The distance dictionary
        distances: Dict[int, List[StationSector]] = dict.fromkeys(range(1, passenger_max_walk_distance), [])

        current_sector_index = current_sector.sector_index
        max_sector_index = self.configuration.station_sector_count

        for i in distances.keys():
            left_sector_index = current_sector_index - i
            right_sector_index = current_sector_index + i

            # Check if the left sector is not out of bounds and
            # that it has a green light. If it does, then we add
            # it to the dictionary.
            if left_sector_index >= 0:
                left_sector = environment.station.sectors[left_sector_index]
                if left_sector.light.status == LightStatus.GREEN:
                    distances[i].append(left_sector)

            # Check if the right sector is not out of bounds and
            # that it has a green light. If it does, then we add
            # it to the dictionary.
            if right_sector_index < max_sector_index:
                right_sector = environment.station.sectors[right_sector_index]
                if right_sector.light.status == LightStatus.GREEN:
                    distances[i].append(right_sector)

        return distances

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
        # Add the passengers who are not compliant back to the from sector
        for i, passenger in enumerate(passengers):
            if not passenger.is_compliant() or passenger.max_walk == 0:
                environment.station.sectors[from_index].add(passengers.pop(i))
        # Move them to the new sector
        environment.station.sectors[to_index].add(passengers)
