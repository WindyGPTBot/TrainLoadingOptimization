from abc import abstractmethod

from Components.Component import Component
from Runtimes.Configuration import Configuration


class PopulatableComponent(Component):
    """
    This is an abstract class for all the components that can be populatable,
    like trains and stations
    """

    def __init__(self, configuration: Configuration):
        """
        Initialize the populatable component. Will run the populate method.
        """
        super().__init__(configuration)
        self.populate()


    @abstractmethod
    def populate(self) -> None:
        """
        Populate the component.
        """
        raise NotImplementedError("Populate method not implemented in " + self.__class__.__name__)

    @abstractmethod
    def amount_passengers(self, follow_through=True) -> int:
        """
        Get the amount of passengers in this object.
        Args:
            follow_through: If True, returns the passenger count after the simulator has run.
        Returns: amount of passengers
        """
        raise NotImplementedError("Populate method not implemented in " + self.__class__.__name__)

