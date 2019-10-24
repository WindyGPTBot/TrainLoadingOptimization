from abc import ABC, abstractmethod
from Runtimes.Environment import Environment
from Runtimes.Configuration import Configuration


class Event(ABC):
    """
    Abstract class that all events must inherit from
    """

    def __init__(self, configuration: Configuration):
        self.configuration = configuration

    @abstractmethod
    def fire(self, environment: Environment) -> None:
        """
        Fire the event
        Args:
            environment: The environment that this event is fired in
        """
        raise NotImplementedError("fire method not implemented in " + self.__class__.__name__)
