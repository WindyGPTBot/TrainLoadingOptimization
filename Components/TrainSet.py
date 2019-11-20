from typing import List

from Runtimes.Configuration import Configuration
from Components.TrainCar import TrainCar


class TrainSet:
    """
    Represents a train set consisting usually of 4 train cars
    """

    def __init__(self, train_cars: List[TrainCar], index: int, configuration: Configuration):
        """
        Initialize a new train set
        Args:
            configuration: The configuration to create the train set with.
        """
        self.__cars = train_cars
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
