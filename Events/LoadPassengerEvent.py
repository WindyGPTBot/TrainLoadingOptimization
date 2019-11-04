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

            # If this is an sector where there is no train parked,
            # but there are waiting passengers then we must move
            # those passengers to a sector where a train is parked.
            if environment.train.parked_at >= sector.sector_index < environment.train.train_car_length:
                return [MovePassengerEvent(sector, self.timestamp, self.configuration)]

            # Get the train car parked at the current sector
            train_car = environment.train[environment.train.parked_at + i]

            # Load the passenger
            passengers = environment.station.sectors[sector.sector_index].remove(1)
            # Security check so that we do not accidentally get an IndexError
            if len(passengers) == 0:
                break
            # Add the passenger to the sector
            train_car.add(passengers[0])
            # The event is only responsible for a single
            # passenger, so we stop the loading in this
            # event once the passenger has been added to
            # the train car.
            break

        # If the station is empty, we can start the departure.
        # Otherwise, there must be other loading events
        # waiting and we therefore just return an empty list.
        if environment.station.is_empty():
            return [PrepareTrainEvent(self.timestamp, self.configuration)]
        else:
            return []
