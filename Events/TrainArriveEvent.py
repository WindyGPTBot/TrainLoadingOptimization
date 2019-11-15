from datetime import datetime
from typing import List, Dict

from Events.Event import Event
from Events.LoadPassengerEvent import LoadPassengerEvent
from Events.MovePassengerEvent import MovePassengerEvent
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

        # We create an event line for each sector, so that we can
        # parallelize each section. This means all cars can start
        # load and unload each car for it self.
        for sector in environment.station.sectors:
            # If the sector has a train car parked, and there are
            # passengers who wants to leave, then we can start
            # unloading. If no passengers are leaving, then we
            # start loading the train car with passenges.
            if sector.has_train_car():
                amount_leaving = passengers_leaving_amount[sector.sector_index]
                if amount_leaving > 0:
                    events.append(UnloadPassengerEvent(sector.train_car,
                                                       sector,
                                                       amount_leaving,
                                                       self.timestamp,
                                                       self.configuration))
                else:
                    events.append(LoadPassengerEvent(sector, self.timestamp, self.configuration))
            else:
                # If no train is parked then we must spawn a move passenger
                # event for each passenger in that sector, so that they can
                # move to a sector where there is a train parked.
                for i in range(sector.amount):
                    events.append(MovePassengerEvent(sector, self.timestamp, self.configuration))

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

        return amounts
