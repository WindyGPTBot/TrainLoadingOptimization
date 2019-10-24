from typing import List

from Components.TrainCar import TrainCar
from Runtimes.Configuration import Configuration


class TrainSet:
    """
    Represents a train set consisting usually of 4 train cars
    """

    def __init__(self, index: int, configuration: Configuration):
        """
        Initialize a new train set
        Args:
            configuration: The configuration to create the train set with.
        """
        self.__cars = self.__spawn_cars(configuration)
        self.__index = index

    @property
    def index(self) -> int:
        """
        Get the index this train set is on the train
        Returns: The train set index
        """
        return self.__index

    @property
    def cars(self) -> List[TrainCar]:
        """
        Get a list containing the train cars in according
        to the train this train set is part of
        Returns: A list with the train cars for this train set
        """
        return self.__cars

    @staticmethod
    def __spawn_cars(configuration: Configuration) -> List[TrainCar]:
        """
        Private static helper method that will spawn the cars for this train set based on the provided configuration
        Args:
            configuration: The configuration used to spawn the cars

        Returns: The spawned list of train cars
        """
        cars = []
        for i in range(configuration.train_set_setup):
            cars.append(TrainCar(i, configuration))
        return cars
