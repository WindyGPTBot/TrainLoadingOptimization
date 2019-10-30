from abc import ABC, abstractmethod
from Runtimes.Environment import Environment
from Runtimes.Configuration import Configuration
import datetime


class Event(ABC):
    """
    Abstract class that all events must inherit from
    """

    def __init__(self, timestamp: datetime, configuration: Configuration):
        self.configuration = configuration
        self.timestamp = timestamp


    @abstractmethod
    def fire(self, environment: Environment) -> list['Event']:
        """
        Fire the event
        Args:
            environment: The environment that this event is fired in
        """
        raise NotImplementedError("fire method not implemented in " + self.__class__.__name__)
