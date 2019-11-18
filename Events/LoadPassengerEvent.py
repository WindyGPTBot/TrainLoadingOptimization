from datetime import datetime
from typing import List

from Components.StationSector import StationSector
from Events.Event import Event
from Events.MovePassengerEvent import MovePassengerEvent
from Events.PrepareTrainEvent import PrepareTrainEvent
from Helpers.Speed import compute_loading_speed
from Runtimes import Configuration
from Runtimes.Environment import Environment


class LoadPassengerEvent(Event):
    """
    Event representing the loading of passengers
    """

    def __init__(self, sector: StationSector, amount: int, timestamp: datetime, configuration: Configuration):
        self.sector: StationSector = sector
        self.amount = amount
        super().__init__(timestamp, configuration)

    def fire(self, environment: Environment) -> List[Event]:
        if self.amount == 0:
            self.logger.info("The amount passed is now zero, so we will stop this loading track")
            return []
        # If this is a sector where there is no train parked,
        # but there are waiting passengers then we must move
        # those passengers to a sector where a train is parked.
        # Or we also want to move passengers wanting
        # to board the train but the train car is full.
        if self.sector.has_train_car() and self.sector.train_car.is_full():
            self.logger.info("Train in sector {} is full. Moving passenger instead.".format(self.sector.sector_index))
            return [MovePassengerEvent(self.sector, self.timestamp, self.configuration)]

        # Get the train car parked at the current sector
        train_car = self.sector.train_car
        # Unload the passenger
        passengers = self.sector.remove(1)
        # Security check so that we do not accidentally get an IndexError
        if len(passengers) == 0:
            self.logger.warning("Removed zero passengers from sector {}".format(self.sector.sector_index))
            return []
        # Add the passenger to the sector
        passenger = passengers[0]
        self.sector.train_car.add(passenger)
        # As with the UnloadPassengerEvent we multiply the
        # loading time with the passenger size to allow
        # simulating two passengers loading at the same time.
        speed = compute_loading_speed(passenger, self.sector.amount)
        # Add the time it takes to load this passenger
        self.do_action(
            speed,
            "Loading passenger {} into car {} in set {} at sector {}".format(passenger.id,
                                                                          train_car.index,
                                                                          train_car.train_set.index,
                                                                          self.sector.sector_index)
        )
        # The event is only responsible for a single
        # passenger, so we stop the loading in this
        # event once the passenger has been added to
        # the train car.
        # If the station is empty, we can start the departure.
        # Otherwise, there must be other passengers waiting
        # so we return another LoadPassengerEvent.
        if environment.station.is_empty() or environment.train.is_full():
            return [PrepareTrainEvent(self.timestamp, self.configuration)]
        elif self.sector.amount > 0:
            return [LoadPassengerEvent(self.sector, self.timestamp, self.configuration)]
        return []
