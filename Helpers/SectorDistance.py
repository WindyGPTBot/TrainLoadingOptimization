from typing import Dict, List, Optional

from Components.LightStatus import LightStatus
from Components.StationSector import StationSector
from Runtimes.Configuration import Configuration
from Runtimes.Environment import Environment


class SectorDistance:
    """
    Class that computes a sort of distance matrix from the provided sector to all other sectors
    """

    def __init__(self, sector: StationSector, environment: Environment, configuration: Configuration):
        self.__sector = sector
        self.__environment = environment
        self.__configuration = configuration
        self.__matrix: Dict[int, Dict[LightStatus, List[StationSector]]] = dict()
        self.__compute()

    def get_closest(self, status: LightStatus) -> Optional[StationSector]:
        """
        Get the closest sector with the provided light status
        Args:
            status: The status of the closest sector
        """
        for distance, matrix in self.__matrix.items():
            if status in matrix and len(matrix[status]) > 0:
                return matrix[status][0]
        return None

    def has_sector_within_distance(self, distance: int, status: LightStatus) -> bool:
        """
        Check if there is a within the distance with the provided status
        Args:
            distance: The distance from the sector
            status: The light status
        Returns:
            True if there is a StationSector within the distance with the given status
        """
        return distance in self.__matrix and status in self.__matrix[distance] and len(
            self.__matrix[distance][status]) > 0

    def get_sector_within_distance(self, distance: int, status: LightStatus, with_least: bool = False) -> StationSector:
        """
        Get the sector within the distance with the provided light status
        Args:
            distance: The distance of the sector
            status: The status of the sector
            with_least: Whether or not to return the sector with least passengers
        Raises:
            IndexError: Thrown if there are no sector within the provided distance,
                or there are no sector with that status within the provided status
        Returns:
            The StationSector with the status within the distance
        """
        if not with_least:
            return self.__matrix[distance][status][0]

        least = self.__matrix[distance][status][0]
        for sector in self.__matrix[distance][status]:
            if sector.amount < least.amount:
                least = sector
        return least

    def __compute(self) -> None:
        """
        Compute the distance matrix
        """
        current_index = self.__sector.sector_index
        left_index = current_index - 1
        right_index = current_index + 1
        current_distance = 1
        # We loop through all the sectors and them to matrix
        for i in range(1, self.__configuration.station_sector_count):
            if left_index >= 0:
                self.__add_sector(self.__environment.station.sectors[left_index], current_distance)
            if right_index < self.__configuration.station_sector_count:
                self.__add_sector(self.__environment.station.sectors[right_index], current_distance)
            current_distance += 1
            left_index -= 1
            right_index += 1

    def __add_sector(self, sector: StationSector, distance: int) -> None:
        """
        Add the sector to the distance matrix
        Args:
            sector: The sector to add
            distance: The distance from the sector
        """
        if distance in self.__matrix and sector.light.status in self.__matrix[distance]:
            self.__matrix[distance][sector.light.status].append(sector)
        else:
            self.__matrix[distance] = {sector.light.status: [sector]}
