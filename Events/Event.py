import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

from Runtimes.Configuration import Configuration
from Runtimes.Environment import Environment


class Event(ABC):
    """
    Abstract class that all events must inherit from
    """

    def __init__(self, timestamp: datetime, configuration: Configuration):
        self.configuration = configuration
        self.timestamp = timestamp

    @abstractmethod
    def fire(self, environment: Environment) -> List[Event]:
        """
        Fire the event
        Args:
            environment: The environment that this event is fired in
        """
        raise NotImplementedError("fire method not implemented in " + self.__class__.__name__)

    def log_event(self):
        logging.info(str(self.timestamp) + " - Finished event: " + self.__class__.__name__)