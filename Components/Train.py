from math import floor
from typing import List

from Components.PopulatableComponent import PopulatableComponent
from Components.TrainCar import TrainCar
from Components.TrainSet import TrainSet
from Helpers.Ranges import random_between_percentage
from Runtimes.Parameters import Parameters
from Runtimes.Configuration import Configuration


class Train(PopulatableComponent):
    """
    This class represents the full train including the train sets and train cars.
    """

    def __init__(self, configuration: Configuration, parameters: Parameters):
        """
        Initialize a new train component
        """
        self.__train_sets = Train.__create_train_sets(configuration, parameters)
        self.__stopped = True
        self.__parked_at = None
        self.__weight = parameters.train_weight
        self.__train_length = len(parameters.train_passengers)
        super().__init__(configuration, parameters)

    def __str__(self):
        return 'Train (w: {}, s: {}, p: {}, l: {})'.format(
            self.weight,
            self.is_stopped(),
            self.parked_at,
            self.train_car_length
        )

    @property
    def parked_at(self) -> int:
        """
        If the train has decided where it is going to be parked,
        get the sector index the first door of the train is parked at.
        Returns: The sector index where the first door is parked
        """
        return self.__parked_at

    @parked_at.setter
    def parked_at(self, sector_index: int):
        """
        Set the sector index where the first door of the train is
        or going to be parked at the station.
        Args:
            sector_index: The sector index where the first door will be
        """
        self.__parked_at = sector_index

    @property
    def train_car_length(self) -> int:
        """
        Get the amount of cars this train carries
        Returns: The total amount of train cars
        """
        if self.__train_length is None:
            self.__train_length = self.configuration.train_set_setup * self.configuration.train_amount_of_sets
        return self.__train_length

    @property
    def train_sets(self) -> List[TrainSet]:
        """
        Get the train sets for this train
        Returns: A list with the train sets
        """
        return self.__train_sets

    @property
    def weight(self) -> float:
        """
        Get the weight of the train
        Returns: The weight as a float
        """
        return self.__weight

    @weight.setter
    def weight(self, weight: float):
        """
        Set the weight of the train
        Args:
            weight: The new weight of the train
        """
        # Let us not allow a minus weight
        if weight < 0:
            weight = 0  # Set it to zero instead
        self.__weight = weight

    def is_stopped(self) -> bool:
        """
        Get whether the train is stopped or driving
        Returns: Boolean representing if the train is stopped (**True**) or driving (**False**)
        """
        return self.__stopped

    def drive(self) -> None:
        """
        Set the train to be driving
        """
        self.__stopped = False

    def stop(self) -> None:
        """
        Set the train to be stopped
        """
        self.__stopped = True

    def populate(self, parameters: Parameters) -> None:
        """
        Populate the train cars with passengers
        """
        if parameters is None:
            rang = self.configuration.train_fullness  # Let us get the range of how full we want our train cars
            cap = self.configuration.train_capacity  # Then we get the max capacity
            for train_set in self.train_sets:
                for car in train_set.cars:
                    # Then we generate a random percentage of the maximum capacity
                    # and then fill the train car with that random amount
                    amount = floor(random_between_percentage(self.configuration.environment_random_seed, rang, cap))
                    car.add(amount, self.configuration)
        else:
            for train_set in self.train_sets:
                for i in range(len(train_set.cars)):
                    train_set.cars[i].add(parameters.train_passengers[i], self.configuration)

    def __getitem__(self, item: int) -> TrainCar:
        """
        Overriden the square bracket index getter so that we can get the
        train car by specifying the total train car index.
        For example: If we specify index 6 with a train set length of 4,
        then we will get the second train car in the second train set.
        Args:
            item: The total train car index
        Returns: The train car at the provided index
        Raises:
            IndexError: Thrown if you provide an invalid index
        """
        set_index = int(item / self.configuration.train_set_setup % self.configuration.train_set_setup)
        car_index = item % self.configuration.train_set_setup
        return self.train_sets[set_index - 1].cars[car_index]

    @staticmethod
    def __create_train_sets(configuration: Configuration, parameters: Parameters) -> List[TrainSet]:
        """
        Create the train sets for this train accordingly to the configuration
        Args:
            configuration: The simulation configuration
        Returns: A list of the newly created train sets
        """
        sets: List[TrainSet] = []
        train_sets_range: range
        if parameters is not None:
            train_sets_range = range(0, int(len(parameters.train_passengers) / 4))
        else:
            train_sets_range = range(configuration.train_amount_of_sets)

        for i in train_sets_range:
            sets.append(TrainSet(i, configuration, parameters))
        return sets
