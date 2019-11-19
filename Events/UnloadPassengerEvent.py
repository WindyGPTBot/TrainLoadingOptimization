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

    def __init__(self, train_car: Optional[TrainCar], sector: StationSector, amount: int, timestamp: datetime,
                 configuration: Configuration):
        self.amount = amount
        self.train_car: Optional[TrainCar] = train_car
        self.sector: StationSector = sector
        super().__init__(timestamp, configuration)

    def fire(self, environment: Environment) -> List[Event]:
        # We must open the door before we can leave
        if not self.train_car.is_open():
            self.train_car.open_door()
            action_time = self.configuration.time_door_action if not UnloadPassengerEvent.DOORS_OPENED else 0
            self.do_action(
                action_time,
                'Opening train car {} door in train set {}'.format(self.train_car.index, self.train_car.train_set.index)
            )
            UnloadPassengerEvent.DOORS_OPENED = True

        passengers_removed = self.train_car.remove(self.amount)

        speed = 0

        for passenger in passengers_removed:
            unloading_speed = compute_loading_speed(passenger, 1)
            speed += unloading_speed

        self.do_action(speed, "Unloaded {} from with car {} in set {} parked in sector {}".format(
            len(passengers_removed), self.train_car.index, self.train_car.train_set.index, self.sector.sector_index))

        # The train is now empty, so now we can
        # start loading passengers into the car.
        return [LoadPassengerEvent(self.sector, self.sector.amount, self.timestamp, self.configuration)]
