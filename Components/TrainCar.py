from Components.Component import Component
from Components.PassengerContainer import PassengerContainer
from Runtimes.Configuration import Configuration


class TrainCar(PassengerContainer, Component):
    """
    Represents a single train car in a train set
    """

    def __init__(self, index: int, car_index: int, configuration: Configuration):
        """
        Initialize a new train car component
        Args:
            configuration: The configuration for which to be used for configuring the train car initialization
        """
        Component.__init__(self, configuration)
        PassengerContainer.__init__(self)
        self.__weight = 0
        self.__opened = False
        self.__train_set = None
        self.__index = index
        self.__car_index = car_index

    @property
    def car_index(self):
        return self.__car_index

    @property
    def train_set(self):
        """
        Get the train that the car is in
        Returns:
            The train set
        """
        return self.__train_set

    @train_set.setter
    def train_set(self, train_set):
        self.__train_set = train_set

    @property
    def index(self) -> int:
        """
        Get the index of this train car in according to the train set it is part of
        Returns: The train car index
        """
        return self.__index

    @property
    def weight(self) -> float:
        """
        Get the weight of the train car.
        Returns: The train car weight
        """
        return self.__weight

    @weight.setter
    def weight(self, value: float):
        """
        Set the weight to provided value
        Args:
            value: The new weight
        """
        self.__weight = value

    @weight.deleter
    def weight(self):
        """
        Reset/Delete the weight by resetting it to zero
        """
        self.__weight = 0

    def is_open(self) -> bool:
        """
        Get the door status, whether it is opened or closed
        Returns: Boolean representing if it is open (**True**) or closed (**False**)
        """
        return self.__opened

    def open_door(self) -> None:
        """
        Open the train car door
        """
        self.__opened = True

    def close_door(self) -> None:
        """
        Close the train car door
        """
        self.__opened = False

    def is_full(self) -> bool:
        """
        Get whether the train car is full
        Returns:
            True if the train car is full, false if it is not.
        """
        return len(self.passengers) == self.configuration.train_capacity
