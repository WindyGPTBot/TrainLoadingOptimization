from typing import List

from Events.Event import Event
from datetime import datetime

from Events.UnloadPassengerEvent import UnloadPassengerEvent
from Helpers.DateTime import add_seconds
from Runtimes.Configuration import Configuration
from Runtimes.Environment import Environment


class TrainArriveEvent(Event):

    def __init__(self, timestamp: datetime, configuration: Configuration):
        super().__init__(timestamp, configuration)

    def __fire(self, environment: Environment) -> List[Event]:
        return [UnloadPassengerEvent(add_seconds(self.timestamp, 0), self.configuration)]
