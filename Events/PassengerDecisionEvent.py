from datetime import datetime
from typing import List

from Components.LightStatus import LightStatus
from Components.StationSector import StationSector
from Events.Event import Event
from Helpers.Distances import sector_distance
from Helpers.Ranges import random_between_range
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
        amount_moved = 0
        moved_to = None
        for passenger in sector.passengers:
            able_distance = self.__time_to_move / passenger.speed

            closest_green_sector = matrix.get_closest(LightStatus.GREEN)
            try:
                green_distance = sector_distance(sector, closest_green_sector)
                can_move_to_green_sector = able_distance >= green_distance
            except TypeError:
                can_move_to_green_sector = False

            closest_yellow_sector = matrix.get_closest(LightStatus.YELLOW)
            try:
                yellow_distance = sector_distance(sector, closest_yellow_sector)
                can_move_to_yellow_sector = able_distance >= yellow_distance
            except TypeError:
                can_move_to_yellow_sector = False

            closest_red_sector = matrix.get_closest(LightStatus.RED)
            try:
                red_distance = sector_distance(sector, closest_red_sector)
                can_move_to_red_sector = able_distance >= red_distance
            except TypeError:
                can_move_to_red_sector = False

            if closest_green_sector is not None and can_move_to_green_sector:
                sector.remove_passenger(passenger)
                closest_green_sector.add(passenger)
                amount_moved += 1
                moved_to = closest_green_sector.sector_index
            elif closest_yellow_sector is not None and can_move_to_yellow_sector:
                sector.remove_passenger(passenger)
                closest_yellow_sector.add(passenger)
                amount_moved += 1
                moved_to = closest_yellow_sector.sector_index
            elif closest_red_sector is not None and can_move_to_red_sector:
                sector.remove_passenger(passenger)
                closest_red_sector.add(passenger)
                amount_moved += 1
                moved_to = closest_red_sector.sector_index
            else:
                self.logger.info(
                    "Could not move passenger {} from sector {} due to no light within able distance".format(
                        passenger.id, sector.sector_index))

        moved_to = moved_to if amount_moved > 0 else sector.sector_index

        self.logger.info(
            "Moved {} passengers from sector {} to {} due to no light".format(amount_moved,
                                                                              sector.sector_index,
                                                                              moved_to))

    def __handle_green_light(self, matrix: SectorDistance, sector: StationSector, environment: Environment) -> None:
        """
        This method handles what the passengers in a section with a green light should do
        Args:
            matrix: The distance matrix from the provided sector
            sector: The sector with the green light
            environment: The simulation environment
        """
        return None

    def __handle_yellow_light(self, matrix: SectorDistance, sector: StationSector, environment: Environment) -> None:
        """
        This method handles what the passengers in a section with a yellow light should do
        Args:
            sector: The sector with the yellow light
            environment: The simulation environment
        """
        # If there is not a green sector right next to the yellow light,
        # then the passengers don't want to move from the yellow sector.
        if not matrix.has_sector_within_distance(1, LightStatus.GREEN):
            return
        # Get the green sector next to the provided sector with the least passengers waiting
        closest_sector = matrix.get_sector_within_distance(1, LightStatus.GREEN, True)

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

            closest_green_sector = matrix.get_closest(LightStatus.GREEN)
            can_move_to_green_sector = able_distance <= sector_distance(sector, closest_green_sector)

            closest_yellow_sector = matrix.get_closest(LightStatus.YELLOW)
            can_move_to_yellow_sector = able_distance <= sector_distance(sector, closest_yellow_sector)

            if closest_green_sector is not None and can_move_to_green_sector:
                sector.remove_passenger(passenger)
                closest_green_sector.add(passenger)
                amount_moved += 1
            elif closest_yellow_sector is not None and can_move_to_yellow_sector:
                sector.remove_passenger(passenger)
                closest_yellow_sector.add(passenger)
                amount_moved += 1
            else:
                closest_red_sector = matrix.get_sector_within_distance(able_distance, LightStatus.RED, True)
                if closest_red_sector.amount < sector.amount:
                    sector.remove_passenger(passenger)
                    closest_red_sector.add(passenger)
                    amount_moved += 1

        self.logger.info("Moved {} passengers from sector {} due to red light".format(amount_moved,
                                                                                      sector.sector_index))
