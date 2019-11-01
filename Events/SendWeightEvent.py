import datetime
from typing import List

from Events.DepartEvent import DepartEvent
from Events.Event import Event
from Events.ReceiveWeightEvent import ReceiveWeightEvent
from Runtimes.Configuration import Configuration
from Runtimes.Environment import Environment


class SendWeightEvent(Event):
    """
    Event when the train gets weighed.
    The train is weighed by summing all the passenger weights together
    """

    def __init__(self, timestamp: datetime, configuration: Configuration):
        super().__init__(timestamp, configuration)

    def fire(self, environment: Environment) -> List[Event]:
        self.log_event()
        return [
            DepartEvent(self.timestamp + datetime.timedelta(seconds=+ self.configuration.time_depart_event),
                        self.configuration),
            ReceiveWeightEvent(
                self.timestamp + datetime.timedelta(seconds=+ self.configuration.time_receive_weight_event),
                self.configuration)
        ]
