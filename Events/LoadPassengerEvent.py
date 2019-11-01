import datetime
from typing import List

from Events.Event import Event
from Runtimes import Configuration
from Runtimes.Environment import Environment


class LoadPassengerEvent(Event):
    """
    Event representing the unloading of passengers
    """
    def __init__(self, timestamp: datetime, configuration: Configuration):
        super().__init__(timestamp, configuration)

    def fire(self, environment: Environment) -> List[Event]:
        self.log_event()
        if not environment.station.is_empty():  # Check if all passengers loaded
            return []
        else:
            return []  # {WeighTrainEvent(self.timestamp + datetime.timedelta(seconds= + self.configuration.time_weight_train_event), self.configuration)}
