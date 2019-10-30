from Events.Event import Event
from Runtimes.Environment import Environment
from Helpers.Ranges import random_between_percentage


class UnloadTrainEvent(Event):
    """
    Event representing the unloading of passengers
    """

    def fire(self, environment: Environment):
        # The configuration that tells us the percentage range
        # of how much each car should randomly unload at the station.
        unload_range = self.configuration.train_unload_percent
        for train_set in environment.train.train_sets:
            for train_car in train_set.cars:
                # We first randomly choose using the configuration
                # how many passengers should leave this car
                passenger_count = len(train_car.passengers)
                nr_leaving = random_between_percentage(unload_range, passenger_count)

                # If there are any passengers leaving we must also
                # open the doors so that passengers can unload.
                if nr_leaving > 0:
                    train_car.open_door()
                    train_car.remove(int(nr_leaving))
