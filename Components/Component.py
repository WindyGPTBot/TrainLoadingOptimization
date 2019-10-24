from abc import ABC

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

    @property
    def configuration(self) -> Configuration:
        """
        Get the simulation configuration
        Returns:
            The simulation configuration
        """
        return self.__configuration

