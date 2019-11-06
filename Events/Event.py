from __future__ import annotations  # To fix Event unresolved reference bug

from logging import getLogger
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

from Helpers.DateTime import add_seconds
from Runtimes.Configuration import Configuration
from Runtimes.Environment import Environment


class Event(ABC):
    """
    Abstract class that all events must inherit from
    """

    def __init__(self, timestamp: datetime, configuration: Configuration):
        self.configuration = configuration
        self.timestamp = timestamp
        self.logger = getLogger(self.__class__.__name__)

    @abstractmethod
    def fire(self, environment: Environment) -> List[Event]:
        """
        Fire the event logic
        Args:
            environment: The environment that this event is fired in
        Returns:
            Returns the next events
        """
        raise NotImplementedError("fire method not implemented in {}".format(self.__class__.__name__))

    def run(self, environment: Environment) -> List[Event]:
        """
        Run the event with the provided environment
        Args:
            environment: The simulation environment
        Returns:
            A list with the next events
        """
        events = self.fire(environment)
        self.log_event()
        return events

    def do_action(self, time: float, description: str = "") -> None:
        """
        Perform an action that takes some time
        Args:
            time: The time it takes to perform the action
            description: Optional description for the action performed. Used mostly for logging.
        """
        # Format message a little bit
        action_descriptor = ": {}".format(description) if description != "" else description
        # Log the action
        self.logger.info("{} performing action that takes {}{}".format(__name__, time, action_descriptor))
        # Add the time to the timestamp
        self.timestamp = add_seconds(self.timestamp, time)

    def log_event(self) -> None:
        """
        Log the event has been run. Is called in self.run()
        """
        self.logger.info("{} - Finished event: {}".format(self.timestamp, self.__class__.__name__))
