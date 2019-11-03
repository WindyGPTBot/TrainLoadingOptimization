from datetime import datetime
from typing import List

from Events.Event import Event
from Events.ReceiveWeightEvent import ReceiveWeightEvent
from Helpers.DateTime import add_seconds
from Runtimes.Configuration import Configuration
from Runtimes.Environment import Environment


class SendWeightEvent(Event):
    """
    Event when the train gets weighed.
    The train is weighed by summing all the passenger weights together
    """

    def __init__(self, timestamp: datetime, configuration: Configuration):
        super().__init__(timestamp, configuration)

    def __fire(self, environment: Environment) -> List[Event]:
        return [
            ReceiveWeightEvent(
                add_seconds(self.timestamp, self.configuration.time_receive_weight_event),
                self.configuration)
        ]
