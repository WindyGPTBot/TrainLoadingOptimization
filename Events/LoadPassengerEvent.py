from datetime import datetime
from typing import List

from Components.StationSector import StationSector
from Components.TrainCar import TrainCar
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
        # If this is a sector where there is no train parked,
        # but there are waiting passengers then we must move
        # those passengers to a sector where a train is parked.
        # Or we also want to move passengers wanting
        # to board the train but the train car is full.
        if self.sector.has_train_car() and self.sector.train_car.is_full():
            self.logger.info("Train in sector {} is full. Moving passenger instead.".format(self.sector.sector_index))
            return [MovePassengerEvent(self.sector, self.sector.amount, self.timestamp, self.configuration)]

        # Get the train car parked at the current sector
        train_car = self.sector.train_car
        # Unload the passenger
        passengers = self.sector.remove(self.amount)
        # Security check so that we do not accidentally get an IndexError
        if len(passengers) == 0:
            self.logger.warning("Removed zero passengers from sector {}".format(self.sector.sector_index))

        total_speed = 0
        amount_to_move = 0
        amount_loaded = 0
        for passenger in passengers:
            # If the train starts getting full,
            # then we must move the amount waiting
            if train_car.is_full():
                amount_to_move += 1
                continue
            # Add the passenger to the sector
            self.sector.train_car.add(passenger)
            # As with the UnloadPassengerEvent we multiply the
            # loading time with the passenger size to allow
            # simulating two passengers loading at the same time.
            speed = compute_loading_speed(passenger, self.sector.amount)
            # Total the amount for loading the passengers
            total_speed += speed
            # For house keeping, we keep track of how many we load
            amount_loaded += 1
        # Add the time it takes to load this passenger
        self.do_action(total_speed,
                       "Loading {} passenger into car {} in set {} at sector {}".format(amount_loaded,
                                                                                        train_car.index,
                                                                                        train_car.train_set.index,
                                                                                        self.sector.sector_index))

        if amount_to_move > 0:
            return [MovePassengerEvent(self.sector, amount_to_move, self.timestamp, self.configuration)]
        elif environment.station.is_empty():
            return [PrepareTrainEvent(self.timestamp, self.configuration)]
        return []
