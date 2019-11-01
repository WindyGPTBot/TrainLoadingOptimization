import datetime
from typing import List

from Events.Event import Event
from Runtimes import Configuration
from Runtimes.Environment import Environment
from Helpers.Ranges import random_between_percentage


class LoadPassengerEvent(Event):
    """
    Event representing the unloading of passengers
    """
    def __init__(self, timestamp: datetime, configuration: Configuration):
        super().__init__(timestamp, configuration)

    def fire(self, environment: Environment) -> List[Event]:
        super().log_event()
        if not environment.station.is_empty(): #Check if all passengers loaded
            return {}
        else:
            return {}#{WeighTrainEvent(self.timestamp, self.configuration)}
