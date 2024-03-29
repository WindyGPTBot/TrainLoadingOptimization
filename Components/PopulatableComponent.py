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

    @property
    def initial_passenger_amount(self) -> int:
        """
        Get the amount of passengers in this object before the simulation finishes.
        Returns: amount of passengers
        """
        raise NotImplementedError("Method not implemented in " + self.__class__.__name__)

    @property
    def final_passenger_amount(self) -> int:
        """
        Get the amount of passengers in this object after the simulation is finished.
        Returns: amount of passengers
        """
        raise NotImplementedError("Method not implemented in " + self.__class__.__name__)

