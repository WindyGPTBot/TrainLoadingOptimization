from typing import Optional

from Components.Component import Component
from Components.Light import Light
from Components.PassengerContainer import PassengerContainer
from Components.TrainCar import TrainCar
from Runtimes.Configuration import Configuration


class StationSector(PassengerContainer, Component):
    """
    Class representing a single station sector which can contain passengers
    """

    def __init__(self, configuration: Configuration, index: int):
        """
        Initialize a new station sector
        """
        self.__index = index
        self.__light = Light(configuration)
        self.__train_car: Optional[TrainCar] = None
        PassengerContainer.__init__(self)
        Component.__init__(self, configuration)

    def __str__(self):
        """
        Giving a nice representation for this object in case print() is called on it.
        Returns: Human-readable string
        """
        return 'Station Sector (i: {}, {})'.format(self.sector_index, self.light)

    @property
    def train_car(self) -> TrainCar:
        """
        Get the train car parked at this sector
        Returns:
            The train car parked at this sector
        """
        return self.__train_car

    @train_car.setter
    def train_car(self, train_car: TrainCar):
        """
        Set the parked train car
        Args:
            train_car: The train car parked at this sector
        """
        self.__train_car = train_car

    def has_train_car(self) -> bool:
        """
        Get whether this station sector has a train car parked
        Returns:
            True if train car is parked at this sector, False if it does not.
        """
        return self.__train_car is not None

    @property
    def light(self) -> Light:
        """
        Get the light component for this sector
        Returns: The light component
        """
        return self.__light

    @property
    def sector_index(self) -> int:
        """
        Get the index for the sector on station.
        Returns: The sector index
        """
        return self.__index

