from datetime import datetime
from typing import List

from Events.Event import Event
from Events.LoadPassengerEvent import LoadPassengerEvent
from Helpers.Ranges import random_between_percentage
from Runtimes import Configuration
from Runtimes.Environment import Environment


class UnloadPassengersEvent(Event):
    """
    Event representing the unloading of passengers
    """

    def __init__(self, timestamp: datetime, configuration: Configuration):
        super().__init__(timestamp, configuration)

    def fire(self, environment: Environment) -> List[Event]:
        door_been_opened = False
        # The configuration that tells us the percentage range
        # of how much each car should randomly unload at the station.
        unload_range = self.configuration.train_unload_percent
        for train_set in environment.train.train_sets:
            for train_car in train_set.cars:
                # We first randomly choose using the configuration
                # how many passengers should leave this car
                passenger_count = len(train_car.passengers)
                nr_leaving = random_between_percentage(
                    self.configuration.environment_random_seed,
                    unload_range,
                    passenger_count
                )

                # If there are any passengers leaving we must also
                # open the doors so that passengers can unload.
                if nr_leaving > 0:
                    train_car.open_door()
                    if not door_been_opened:
                        self.do_action(self.configuration.time_door_action,
                                       "Opening door for unloading")
                        door_been_opened = True
                    train_car.remove(int(nr_leaving))
                    self.logger.info(
                        "Removing {} passengers from train car {} in train set {}".format(
                            int(nr_leaving), train_car.index, train_set.index)
                    )

        return [LoadPassengerEvent(self.timestamp, self.configuration)]
