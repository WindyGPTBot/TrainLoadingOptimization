import datetime
from typing import List

from Events.Event import Event
from Events.ReceiveWeightEvent import ReceiveWeightEvent
from Events.UnloadPassengerEvent import UnloadTrainEvent
from Runtimes.Configuration import Configuration
from Runtimes.Environment import Environment


class ArriveEvent(Event):
    """
    Event when the train gets weighed.
    The train is weighed by summing all the passenger weights together
    """
    def __init__(self, timestamp: datetime, configuration: Configuration):
        super().__init__(timestamp, configuration)

    def fire(self, environment: Environment) -> List[Event]:
        return {UnloadTrainEvent(self.timestamp, self.configuration)}