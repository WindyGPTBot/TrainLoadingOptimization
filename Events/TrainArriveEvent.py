from typing import List

from Events.Event import Event
from datetime import datetime

from Events.UnloadPassengerEvent import UnloadPassengerEvent
from Helpers.DateTime import add_seconds
from Runtimes.Configuration import Configuration
from Runtimes.Environment import Environment


class TrainArriveEvent(Event):
    """
    Event that represents when the train arrives at the station
    """
    def __init__(self, timestamp: datetime, configuration: Configuration):
        """
        Initialize a new TrainArriveEvent
        Args:
            timestamp: The timestamp when this event happens
            configuration: The simulation configuration
        """
        super().__init__(timestamp, configuration)

    def __fire(self, environment: Environment) -> List[Event]:
        return [UnloadPassengerEvent(add_seconds(self.timestamp, 0), self.configuration)]
