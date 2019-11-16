from datetime import datetime
from typing import List, Optional

from Components.StationSector import StationSector
from Components.TrainCar import TrainCar
from Events.Event import Event
from Events.LoadPassengerEvent import LoadPassengerEvent
from Runtimes.Configuration import Configuration
from Runtimes.Environment import Environment
from Helpers.Speed import compute_loading_speed


class UnloadPassengerEvent(Event):
    """
    Event representing a single passenger leaving the train
    """
    DOORS_OPENED = False

    def __init__(self, train_car: Optional[TrainCar], sector: StationSector, amount: int, timestamp: datetime, configuration: Configuration):
        self.amount = amount
        self.train_car: Optional[TrainCar] = train_car
        self.sector: StationSector = sector
        super().__init__(timestamp, configuration)

    def fire(self, environment: Environment) -> List[Event]:
        # It is really no problem that this happens,
        # but there is no reason for it to happen,
        # so we should try to avoid it, but let
        # us just log it for now.
        if self.train_car.amount <= 0:
            self.logger.warning("We are trying to unload an empty train.")
            return []

        # We must open the door before we can leave
        if not self.train_car.is_open():
            self.train_car.open_door()
            self.do_action(
                self.configuration.time_door_action if not self.DOORS_OPENED else 0,
                'Opening train car {} door in train set {}'.format(self.train_car.index, self.train_car.train_set.index)
            )

        # Remove the passenger from the car
        passengers_removed = self.train_car.remove(1)
        # Let us just be sure we know what we are doing
        amount_removed = len(passengers_removed)
        if amount_removed != 1:
            raise RuntimeError("The car was not empty, but we retrieved {} passengers.".format(amount_removed))
        # Otherwise, we can continue
        passenger = passengers_removed[0]
        # The speed is computed by multiplying the passenger
        # size with the loading time. This means that if we
        # define the passenger size to be 0.5 and the time it
        # takes to unload a passenger is 2 seconds, then we can
        # unload two passengers in the seconds so that we "simulate"
        # that we unload two passengers at a time, but we are versatile
        # to make this work for any size of passengers.
        speed = compute_loading_speed(passenger, self.amount)
        action_description = 'Unloading passenger from train car {} in train set {}'.format(
            self.train_car.index, self.train_car.train_set.index)
        # Do the loading action that adds the time to the timestamp
        self.do_action(speed, action_description)

        # If the train is now empty, meaning that this passenger
        # was last, then we start loading into the car. Else, we
        # just continue the unloading
        if self.train_car.amount == 0 or self.amount == 0:
            return [LoadPassengerEvent(self.sector, self.timestamp, self.configuration)]
        else:
            return [UnloadPassengerEvent(
                self.train_car,
                self.sector,
                self.amount - 1,
                self.timestamp,
                self.configuration)]
