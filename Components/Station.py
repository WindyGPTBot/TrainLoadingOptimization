from math import floor
from typing import List, Tuple

from Components.PopulatableComponent import PopulatableComponent
from Components.StationSector import StationSector
from Helpers.Ranges import random_between_percentage
from Runtimes.Parameters import Parameters
from Runtimes.Configuration import Configuration


class Station(PopulatableComponent):
    """
    Class representing the station component containing the station sectors
    """

    def __init__(self, configuration: Configuration, parameters: Parameters):
        """
        Initialize a new station
        Args:
            configuration: The configuration to create the station with
        """
        self.__sectors = Station.__create_sectors(configuration, parameters)
        super().__init__(configuration, parameters)

    def __str__(self):
        return 'Station ({})'.format(', '.join([str(x) for x in self.sectors]))

    def populate(self, parameters: Parameters) -> None:
        """
        Populate the station sectors
        """
        # First, we get a list with integers that represent which sectors that have stairs
        stair_placement = self.configuration.station_stairs_placement
        total_waiting = 0
        if parameters is not None:
            for sector in self.sectors:
                # First we get the distances to all the stairs
                distances = self.__calculate_distances(sector.sector_index, stair_placement)

                # Get the lowest distance by the distance key in the tuple
                ld_index, ld_distance = min(distances, key=lambda x: x[1])
                rang = self.configuration.station_sector_fullness  # The range that defines the percentage range
                cap = self.configuration.station_sector_passenger_max_count  # The sector max capacity
                # The stair factor which defines the importance of the stair
                stair_factor = self.configuration.station_stair_factor
                # Calculate the amount of people in this sector based on the parameters above
                amount = floor(
                    random_between_percentage(
                        self.configuration.environment_random_seed,
                        rang,
                        cap
                    ) - ld_distance * stair_factor
                )
                # Sometimes we end up with a amount < 0, let us just set it to zero then
                if amount < 0:
                    amount = 0
                # Add the amount to the sector
                sector.add(amount, self.configuration)
                total_waiting += amount
                self.logger.info("There are {} passengers waiting in sector {}".format(amount, sector.sector_index))
        else:
            for i in range(0,len(self.sectors)):
                self.sectors[i].add(parameters.station_passengers[i])
                total_waiting += parameters.station_passengers[i]
                self.logger.info("There are {} passengers waiting in sector {}".format(parameters.station_passengers[i], self.sectors[i].sector_index))
        self.logger.info("There in total {} passengers waiting on the station".format(total_waiting))

    @property
    def sectors(self) -> List[StationSector]:
        """
        Get the list of station sectors
        Returns: List containing the individual station sectors
        """
        return self.__sectors

    @staticmethod
    def __calculate_distances(sector_index: int, stair_placements: List[int]) -> List[Tuple[int, int]]:
        """
        Calculate the distance from the given sector index to all the stair placements.
        Args:
            sector_index: The sector index to calculate the distances from
            stair_placements: A list with indexes for all the stairs on the station
        Returns: A list with tuples with the information: (stair_index, distance_to_stair)
        """
        distances: List[Tuple[int, int]] = []

        for placement in stair_placements:
            distances.append((placement, abs(placement - sector_index)))

        return distances

    @staticmethod
    def __create_sectors(configuration: Configuration, parameters: Parameters) -> List[StationSector]:
        """
        Private static helper method to populate the station sectors
        """
        sectors = []
        sector_count: range
        if parameters is not None:
            sector_count = range(len(parameters.station_passengers))
        else:
            sector_count = range(configuration.train_amount_of_sets)

        for i in sector_count:
            sectors.append(StationSector(configuration, parameters, i))
        return sectors

    def is_empty(self) -> bool:
        """
        Get whether the station has any passengers in any sector
        Returns:
            True if the station is empty, False if there is > 0 passengers in any sector.
        """
        for s in self.sectors:
            if len(s.passengers) > 0:
                return False
        return True
