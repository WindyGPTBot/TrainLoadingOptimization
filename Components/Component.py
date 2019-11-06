from abc import ABC
from logging import getLogger

from Runtimes.Configuration import Configuration


class Component(ABC):
    """
    Abstract class that all the components must inherit from
    """

    def __init__(self, configuration: Configuration):
        """
        Abstract constructor for the component.
        Should not be used directly!
        """
        self.__configuration = configuration
        self.logger = getLogger(self.__class__.__name__)

    def __repr__(self):
        return self.__str__()

    @property
    def configuration(self) -> Configuration:
        """
        Get the simulation configuration
        Returns:
            The simulation configuration
        """
        return self.__configuration

