from datetime import datetime
from typing import List

from Events.Event import Event
from Runtimes.Configuration import Configuration
from Runtimes.Environment import Environment


class PrepareTrainEvent(Event):
    """
    Before the train can depart the station, we must prepare it for departure.
    This includes closing the doors and whatever we may think of.
    """
    def __init__(self, timestamp: datetime, configuration: Configuration):
        super().__init__(timestamp, configuration)

    def __fire(self, environment: Environment) -> List[Event]:

        for train_set in environment.train.train_sets:
            for train_car in train_set.cars:
                # We must close the door if it has been opened.
                if train_car.is_open():
                    train_car.close_door()

        return []

