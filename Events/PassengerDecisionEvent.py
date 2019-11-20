from datetime import datetime
from typing import List

from Components.LightStatus import LightStatus
from Components.StationSector import StationSector
from Events.Event import Event
from Helpers.Distances import sector_distance
from Helpers.Ranges import random_between_range, random_choice
from Helpers.SectorDistance import SectorDistance
from Runtimes import Configuration
from Runtimes.Environment import Environment


class PassengerDecisionEvent(Event):
    """
    Event that represents when a passenger on the station must make
    a decision based on the new light status. This event will also
    be responsible for moving the passengers on the station around
    based on their decisions.
    """

    def __init__(self, timestamp: datetime, train_arrives: datetime, configuration: Configuration):
        super().__init__(timestamp, configuration)
        self.__train_arrives = train_arrives
        self.__time_to_move = (train_arrives - timestamp).total_seconds()

    def fire(self, environment: Environment) -> List[Event]:
        for sector in environment.station.sectors:
            matrix = SectorDistance(sector, environment, self.configuration)
            light_status = sector.light.status
            # The passengers stay if they are in a green sector
            if light_status == LightStatus.GREEN:
                self.__handle_green_light(matrix, sector, environment)
            elif light_status == LightStatus.YELLOW:
                self.__handle_yellow_light(matrix, sector, environment)
            elif light_status is None:
                self.__handle_none_light(matrix, sector, environment)
            else:
                self.__handle_red_light(matrix, sector, environment)
        return []

    def __handle_none_light(self, matrix: SectorDistance, sector: StationSector, environment: Environment) -> None:
        for i in range(sector.amount):
            # Remove the passenger from the current sector
            passenger = sector.remove(1)[0]
            # Compute the distance they are able to walk
            able_distance = self.__time_to_move / passenger.speed
            # Get how far the passenger is willing to walk
            willing_distance = passenger.max_walk
            # If the passenger is not willing to walk as far
            # as he is able, we will restrict how far he is
            # able to walk by the distance he is willing to walk.
            if willing_distance < able_distance:
                able_distance = willing_distance
            # Now we can find all the available sectors that the passenger can move to
            available_sectors = []
            available_sectors.extend(matrix.get_sectors_within_distance(able_distance, LightStatus.GREEN))
            available_sectors.extend(matrix.get_sectors_within_distance(able_distance, LightStatus.YELLOW))
            available_sectors.extend(matrix.get_sectors_within_distance(able_distance, LightStatus.RED))

            if len(available_sectors) > 0:
                chosen_sector = available_sectors[0]
                for available_sector in available_sectors:
                    if available_sector.amount < chosen_sector.amount:
                        chosen_sector = available_sector
            else:
                self.logger.warning("Chosen to move to a sector without lights")
                chosen_sector = sector
            self.logger.info("Moved passenger from {} to {} due to no light".format(sector.sector_index,
                                                                                    chosen_sector.sector_index))
            chosen_sector.add(passenger)

    def __handle_green_light(self, matrix: SectorDistance, sector: StationSector, environment: Environment) -> None:
        """
        This method handles what the passengers in a section with a green light should do
        Args:
            matrix: The distance matrix from the provided sector
            sector: The sector with the green light
            environment: The simulation environment
        """
        return None

    def __handle_yellow_light(self, matrix: SectorDistance, sector: StationSector,
                              environment: Environment) -> None:
        """
        This method handles what the passengers in a section with a yellow light should do
        Args:
            sector: The sector with the yellow light
            environment: The simulation environment
        """
        # If there is not a green sector right next to the yellow light,
        # then the passengers don't want to move from the yellow sector.
        if not matrix.has_sector_within_distance(2, LightStatus.GREEN):
            return
        # Get the green sector next to the provided sector with the least passengers waiting
        closest_sector = matrix.get_sector_within_distance(2, LightStatus.GREEN, True)

        move_amount = random_between_range(
            self.configuration.environment_random_seed,
            range(0, environment.station.sectors[closest_sector.sector_index].amount)
        )

        # Remove the passengers that will move from the provided sector
        removed_passengers = sector.remove(move_amount)

        # Add the removed passengers to the other sectors
        closest_sector.add(removed_passengers)

        self.logger.info(
            "Moved {} passengers from sector {} to sector {} because of yellow light".format(move_amount,
                                                                                             sector.sector_index,
                                                                                             closest_sector.sector_index))

    def __handle_red_light(self, matrix: SectorDistance, sector: StationSector, environment: Environment) -> None:
        """
        This method handles what the passengers in a section with a red light should do
        Args:
            sector: The sector with the red light
            environment: The simulation environment
        """
        amount_moved = 0
        for passenger in sector.passengers:
            able_distance = self.__time_to_move / passenger.speed

            closest_green_sector = matrix.get_sector_within_distance(able_distance, LightStatus.GREEN, True)
            try:
                green_distance = sector_distance(sector, closest_green_sector)
                can_move_to_green_sector = able_distance <= green_distance
            except TypeError:
                can_move_to_green_sector = False

            closest_yellow_sector = matrix.get_sector_within_distance(able_distance, LightStatus.YELLOW, True)
            try:
                yellow_distance = sector_distance(sector, closest_yellow_sector)
                can_move_to_yellow_sector = able_distance <= yellow_distance
            except TypeError:
                can_move_to_yellow_sector = False

            if closest_green_sector is not None and can_move_to_green_sector:
                sector.remove_passenger(passenger)
                closest_green_sector.add(passenger)
                amount_moved += 1
            elif closest_yellow_sector is not None and can_move_to_yellow_sector:
                sector.remove_passenger(passenger)
                closest_yellow_sector.add(passenger)
                amount_moved += 1

        self.logger.info("Moved {} passengers from sector {} due to red light".format(amount_moved,
                                                                                      sector.sector_index))
