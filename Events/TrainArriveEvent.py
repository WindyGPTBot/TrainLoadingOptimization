from datetime import datetime
from typing import List

from Events.Event import Event
from Events.UnloadPassengersEvent import UnloadPassengersEvent
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

    def fire(self, environment: Environment) -> List[Event]:
        environment.timings.start_timer(self.timestamp)
        return [UnloadPassengersEvent(add_seconds(self.timestamp, 0), self.configuration)]
