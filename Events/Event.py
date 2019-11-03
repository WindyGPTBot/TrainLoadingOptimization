from __future__ import annotations
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
        self.logger = logging.getLogger(__name__)

    @abstractmethod
    def __fire(self, environment: Environment) -> List[Event]:
        """
        Fire the event logic
        Args:
            environment: The environment that this event is fired in
        Returns:
            Returns the next events
        """
        raise NotImplementedError("fire method not implemented in " + self.__class__.__name__)

    def run(self, environment: Environment) -> List[Event]:
        """
        Run the event with the provided environment
        Args:
            environment: The simulation environment
        Returns:
            A list with the next events
        """
        self.log_event()
        return self.__fire(environment)

    def log_event(self):
        logging.info(str(self.timestamp) + " - Finished event: " + self.__class__.__name__)
