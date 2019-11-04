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

        # Generate a LoadPassengerEvent for each passenger
        # waiting on the platform. First we sum the amount
        # of passengers waiting, and then we generate the list.
        total_amount_to_load = 0
        for sector in environment.station.sectors:
            total_amount_to_load += sector.amount
        # Instantiate the LoadPassengerEvent objects
        events = []
        for i in range(total_amount_to_load):
            events.append(LoadPassengerEvent(self.timestamp, self.configuration))
        # Return the events as we should load after unloading
        return events
