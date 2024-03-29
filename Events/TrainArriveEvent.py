from datetime import datetime
from typing import List, Dict

from Events.Event import Event
from Events.LoadPassengerEvent import LoadPassengerEvent
from Events.MovePassengerEvent import MovePassengerEvent
from Events.UnloadPassengerEvent import UnloadPassengerEvent
from Helpers.DateTime import add_seconds
from Helpers.Speed import compute_loading_speed
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
            if sector.has_train_car():
                amount_leaving = passengers_leaving_amount[sector.sector_index]
                if amount_leaving > 0:
                    events.append(
                        UnloadPassengerEvent(sector.train_car, sector, amount_leaving, self.timestamp,
                                             self.configuration))
                    self.logger.info("Unloading {} in sector {}".format(amount_leaving, sector.sector_index))
                else:
                    events.append(
                        LoadPassengerEvent(sector, sector.amount, self.timestamp, self.configuration))
                    self.logger.info("Loading {} in sector {}".format(sector.amount, sector.sector_index))
            elif sector.amount > 0:
                events.append(MovePassengerEvent(sector, sector.amount, self.timestamp, self.configuration))
                self.logger.info("Moving {} in sector {}".format(sector.amount, sector.sector_index))
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
                passenger_count = train_car.amount
                if isinstance(self.configuration.train_unload_percent, (list, dict)):
                    percent_leaving = self.configuration.train_unload_percent[
                        sector_index - environment.train.parked_at]
                    nr_leaving = (percent_leaving / 100) * passenger_count
                    amounts[sector_index] = int(nr_leaving)
                else:
                    # We first randomly choose using the configuration
                    # how many passengers should leave this car
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
