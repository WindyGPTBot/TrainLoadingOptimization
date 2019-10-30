import datetime

from Events.Event import Event
from Events.ReceiveWeightEvent import ReceiveWeightEvent
from Runtimes.Configuration import Configuration
from Runtimes.Environment import Environment


class WeighTrainEvent(Event):
    """
    Event when the train gets weighed.
    The train is weighed by summing all the passenger weights together
    """
    def __init__(self, timestamp: datetime, configuration: Configuration) -> list[Event]:
        super().__init__(timestamp, configuration)

    def fire(self, environment: Environment):
        # Adding all the passengers weights together
        # and storing it in the train weight property
        for train_set in environment.train.train_sets:
            for train_car in train_set.cars:
                for passenger in train_car.passengers:
                    train_car.weight += passenger.weight
                environment.train.weight += train_car.weight
        return {ReceiveWeightEvent(self.timestamp + datetime.timedelta(seconds=2), self.configuration)}