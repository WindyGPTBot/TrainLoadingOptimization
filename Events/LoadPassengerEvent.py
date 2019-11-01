import datetime
from typing import List

from Events.Event import Event
from Events.WeighTrainEvent import WeighTrainEvent
from Helpers.DateTime import add_seconds
from Runtimes import Configuration
from Runtimes.Environment import Environment


class LoadPassengerEvent(Event):
    """
    Event representing the unloading of passengers
    """
    def __init__(self, timestamp: datetime, configuration: Configuration):
        super().__init__(timestamp, configuration)

    def __fire(self, environment: Environment) -> List[Event]:
        if not environment.station.is_empty():  # Check if all passengers loaded
            return []
        else:
            return [WeighTrainEvent(add_seconds(self.timestamp, 0), self.configuration)]
