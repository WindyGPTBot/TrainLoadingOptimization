from typing import List

from Runtimes.Parameters import Parameters
from Runtimes.Configuration import Configuration
from Components.TrainCar import TrainCar


class TrainSet:
    """
    Represents a train set consisting usually of 4 train cars
    """

    def __init__(self, index: int, configuration: Configuration, parameters: Parameters):
        """
        Initialize a new train set
        Args:
            configuration: The configuration to create the train set with.
        """
        self.__cars = self.__spawn_cars(configuration, parameters)
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

    def __spawn_cars(self, configuration: Configuration, parameters: Parameters) -> List[TrainCar]:
        """
        Private static helper method that will spawn the cars for this train set based on the provided configuration
        Args:
            configuration: The configuration used to spawn the cars

        Returns: The spawned list of train cars
        """
        cars = []
        cars_count_range: range
        if parameters is None:
            cars_count_range = range(configuration.train_amount_of_sets)
        else:
            cars_count_range = range(0, len(parameters.train_passengers))

        for i in cars_count_range:
            cars.append(TrainCar(i, configuration, parameters, self))
        return cars
