from datetime import datetime
from typing import List

from Events.Event import Event
from Events.MovePassengerEvent import MovePassengerEvent
from Events.PrepareTrainEvent import PrepareTrainEvent
from Runtimes import Configuration
from Runtimes.Environment import Environment


class LoadPassengerEvent(Event):
    """
    Event representing the loading of passengers
    """

    def __init__(self, timestamp: datetime, configuration: Configuration):
        super().__init__(timestamp, configuration)

    def fire(self, environment: Environment) -> List[Event]:

        for i, sector in enumerate(environment.station.sectors):
            # If the current sector is empty, then we continue
            # until we get a sector which have waiting passengers.
            if sector.amount == 0:
                continue

            # If this is a sector where there is no train parked,
            # but there are waiting passengers then we must move
            # those passengers to a sector where a train is parked.
            if not sector.has_train_car():
                self.logger.info("No train at sector {}. Moving passenger instead.".format(sector.sector_index))
                return [MovePassengerEvent(sector, self.timestamp, self.configuration)]
            # Or we also want to move passengers wanting
            # to board the train but the train car is full.
            elif sector.train_car.is_full():
                self.logger.info("Train in sector {} is full. Moving passenger instead.".format(sector.sector_index))
                return [MovePassengerEvent(sector, self.timestamp, self.configuration)]

            # Get the train car parked at the current sector
            train_car = sector.train_car
            # Unload the passenger
            passengers = environment.station.sectors[sector.sector_index].remove(1)
            # Security check so that we do not accidentally get an IndexError
            if len(passengers) == 0:
                self.logger.warning("Unloaded zero passengers from section {}".format(sector.sector_index))
                break
            # Add the passenger to the sector
            train_car.add(passengers[0])
            # Add the time it takes to load this passenger
            self.do_action(
                passengers[0].loading_time,
                "Loading passenger into car {} in set {}".format(train_car.index, train_car.train_set.index)
            )
            # The event is only responsible for a single
            # passenger, so we stop the loading in this
            # event once the passenger has been added to
            # the train car.
            break

        # If the station is empty, we can start the departure.
        # Otherwise, there must be other passengers waiting
        # so we return another LoadPassengerEvent.
        if environment.station.is_empty():
            return [PrepareTrainEvent(self.timestamp, self.configuration)]
        else:
            return [LoadPassengerEvent(self.timestamp, self.configuration)]
