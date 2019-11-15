from abc import abstractmethod

from Components.Component import Component
from Runtimes.Parameters import Parameters
from Runtimes.Configuration import Configuration


class PopulatableComponent(Component):
    """
    This is an abstract class for all the components that can be populatable,
    like trains and stations
    """

    def __init__(self, configuration: Configuration, parameters: Parameters):
        """
        Initialize the populatable component. Will run the populate method.
        """
        super().__init__(configuration)
        self.populate(parameters)

    @abstractmethod
    def populate(self, parameters: Parameters) -> None:
        """
        Populate the component.
        """
        raise NotImplementedError("Populate method not implemented in " + self.__class__.__name__)

