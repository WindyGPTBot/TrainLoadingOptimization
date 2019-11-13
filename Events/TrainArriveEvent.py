from datetime import datetime
from typing import List, Dict

from Events.Event import Event
from Events.LoadPassengerEvent import LoadPassengerEvent
from Events.UnloadPassengerEvent import UnloadPassengerEvent
from Events.UnloadPassengersEvent import UnloadPassengersEvent
from Helpers.DateTime import add_seconds
from Helpers.Ranges import random_between_percentage
from Runtimes.Configuration import Configuration
from Runtimes.Environment import Environment


class TrainArriveEvent(Event):
    """
    Event that represents when the train arrives at the station
    """
    def __init__(self, timestamp: datetime, configuration: Configuration):
        """
        Initialize a new TrainArriveEvent
        Args:
            timestamp: The timestamp when this event happens
            configuration: The simulation configuration
        """
        super().__init__(timestamp, configuration)

    def fire(self, environment: Environment) -> List[Event]:
        # We start the turn around timer when
        # the train arrives at the station.
        environment.timings.start_timer(self.timestamp)

        # Let us figure how many of UnloadPassengerEvent and
        # LoadPassengerEvent events we should initialize.
        passengers_leaving_amount = self.__decide_unloading_count(environment)
        # This is where we store the events we create under here
        events = []

        # We loop through the passengers_leaving_amount that maps
        # the sector index to amount of passengers leaving the
        # train car which is parked at that station sector index.
        # If there are zero passengers leaving at a sector, then
        # we can start loading passengers into that car.
        for index, amount in passengers_leaving_amount.items():
            sector = environment.station.sectors[index]
            if amount > 0:
                events.append(
                    UnloadPassengerEvent(sector.train_car, sector, amount, self.timestamp, self.configuration))
            else:
                events.append(LoadPassengerEvent(sector, self.timestamp, self.configuration))

        return events

    def __decide_unloading_count(self, environment: Environment) -> Dict[int, int]:
        """
        Private method that calculates how many passengers leaves each train car.
        Args:
            environment: The simulation environment.
        Returns:
            A dictionary that maps the sector index to how many
            leaves from the train car at that station sector.
        """
        unload_range = self.configuration.train_unload_percent

        sector_index = environment.train.parked_at

        amounts: Dict[int, int] = dict()

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
                # Add the amount leaving mapped by the sector index
                amounts[sector_index] = int(nr_leaving)
                # Increment the indexes
                sector_index += 1
            sector_index += 1

        return amounts
