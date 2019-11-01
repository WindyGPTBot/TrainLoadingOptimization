import datetime
from typing import List

from Events.ArriveEvent import ArriveEvent
from Events.Event import Event
from Runtimes.Configuration import Configuration
from Runtimes.Environment import Environment


class DepartEvent(Event):
    """
    Event when the train gets weighed.
    The train is weighed by summing all the passenger weights together
    """
    def __init__(self, timestamp: datetime, configuration: Configuration):
        super().__init__(timestamp, configuration)

    def fire(self, environment: Environment) -> List[Event]:
        self.log_event()
        return [
            ArriveEvent(self.timestamp + datetime.timedelta(seconds= + self.configuration.time_arrive_event),
                        self.configuration)
        ]
