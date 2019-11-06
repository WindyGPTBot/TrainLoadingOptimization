from datetime import datetime
from typing import List

from Events.Event import Event
from Events.ReceiveWeightEvent import ReceiveWeightEvent
from Events.TrainArriveEvent import TrainArriveEvent
from Helpers.Acceleration import compute_driving_time
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

    def fire(self, environment: Environment) -> List[Event]:
        train_arrive_time = add_seconds(self.timestamp, compute_driving_time(self.configuration.station_distance))
        return [
            ReceiveWeightEvent(
                add_seconds(self.timestamp, self.configuration.time_receive_weight_event),
                train_arrive_time,
                self.configuration
            ),
            TrainArriveEvent(
                train_arrive_time,
                self.configuration
            )
        ]
