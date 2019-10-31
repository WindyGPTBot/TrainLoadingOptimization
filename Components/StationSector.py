from Components.Component import Component
from Components.Light import Light
from Components.PassengerContainer import PassengerContainer
from Runtimes.Configuration import Configuration


class StationSector(PassengerContainer):
    """
    Class representing a single station sector which can contain passengers
    """

    def __init__(self, configuration: Configuration, index: int):
        """
        Initialize a new station sector
        """
        self.__index = index
        self.__light = Light(configuration)
        super().__init__()

    def __str__(self):
        """
        Giving a nice representation for this object in case print() is called on it.
        Returns: Human-readable string
        """
        return 'Station Sector (i: {}, {})'.format(self.sector_index, self.light)

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

