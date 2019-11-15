from typing import Dict, List, Union
from Distributions.Distribution import Distribution


class Parameters:
    """
    This class represents all the parameters for int initialization of the simulation
    """

    def __init__(self, params: Dict):
        """
        Initialize the parameters
        Args:
            options: A dictionary containing all the parameters
        """
        self.__params = params

    @property
    def lights(self) -> bool:
        """
        Whether the stations will have lights or not
        """
        return self.__params['lights']

    @property
    def train_passengers(self) -> list:
        """
        Get the weight of the passengers on the train
        Returns: A list of lists. The list contains one list for each wagon, which contains all the weights of the passengers in that wagon
        """
        return self.__options['train']

    @property
    def train_weight(self) -> float:
        """
        Get the weight of the train itself
        Returns:
            float representing the weight in kilograms
        """
        return self.__options['train_weight']

    @property
    def station_passengers(self) -> list:
        """
        Get the weight of the passengers on the station
        Returns: A list of lists. The list contains one list for each sector, which contains all the weights of the passengers in that sector
        """
        return self.__options['station']

    @property
    def station_distance(self) -> float:
        """
        Get the distance from the train to the station
        Returns:
            a float representing the distance in kilometers
        """
        return self.__options['station_distance']