from typing import Union

from Components.Station import Station
from Components.StationSector import StationSector
from Components.Train import Train
from Components.TrainCar import TrainCar
from Runtimes.Parameters import Parameters
from Runtimes.Configuration import Configuration
from Runtimes.Timing import Timing


class Environment:
    """
    Class holding all the components in the environment.
    """
    def __init__(self, configuration: Configuration, parameters: Parameters):
        self.__configuration: Configuration = configuration
        self.__train: Train = Train(configuration, parameters)
        self.__station: Station = Station(configuration, parameters)
        self.__timings: Timing = Timing()

    @property
    def configuration(self) -> Configuration:
        """
        Get the environment configuration
        Returns: The configuration
        """
        return self.__configuration

    @property
    def train(self) -> Train:
        """
        Get the environment train
        Returns: The train
        """
        return self.__train

    @property
    def station(self) -> Station:
        """
        Get the environment station
        Returns: The station
        """
        return self.__station

    @property
    def timings(self) -> Timing:
        """
        Get the environment timings
        Returns: The timings
        """
        return self.__timings

    def get_train_car_at_sector(self, sector: Union[StationSector, int]) -> TrainCar:
        """
        Get the train car parked at the given sector
        Args:
            sector: The sector where the train car is parked.
                Can be either the *StationSector* object, or just the actual index.
        Raises:
            IndexError: Thrown if there is no train car parked at the given sector or index
        Returns:
            The train car at the provided sector.
        """
        index = sector.sector_index if isinstance(sector, StationSector) else sector
        car_index = index - self.train.parked_at
        try:
            return self.train[car_index]
        except IndexError as e:
            raise IndexError("There is no train car parked at sector {}".format(index)) from e
