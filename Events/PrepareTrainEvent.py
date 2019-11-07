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

    def fire(self, environment: Environment) -> List[Event]:
        has_been_opened = False

        for train_set in environment.train.train_sets:
            for train_car in train_set.cars:
                # We must close the door if it has been opened.
                if train_car.is_open():
                    train_car.close_door()
                    # Since closing the doors is done all at once
                    # we just check if the door has been opened once
                    # and if they have then we just continue, otherwise
                    # we add 4 seconds of time taken.
                    if not has_been_opened:
                        self.do_action(self.configuration.time_door_action, "Closing the doors")
                        has_been_opened = True
        # Stop the timer once this event has concluded,
        # as we do not care about weighing the train again
        environment.timings.stop_timer(self.timestamp)
        return []

