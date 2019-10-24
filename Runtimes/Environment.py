from Components.Station import Station
from Components.Train import Train
from Runtimes.Configuration import Configuration
from Runtimes.Timing import Timing


class Environment:
    """
    Class holding all the components in the environment.
    """
    def __init__(self, configuration: Configuration):
        self.__configuration: Configuration = configuration
        self.__train: Train = Train(configuration)
        self.__station: Station = Station(configuration)
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
