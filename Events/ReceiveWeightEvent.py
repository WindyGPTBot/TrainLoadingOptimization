import datetime
from typing import List

from Components.LightStatus import LightStatus
from Events.Event import Event
from Events.PassengerDecisionEvent import PassengerDecisionEvent
from Runtimes.Configuration import Configuration
from Runtimes.Environment import Environment
from Helpers.Ranges import random_between_range


class ReceiveWeightEvent(Event):
    """
    Receive weight information event.
    This event is responsible for receiving the weight information,
    and then lighting the station lights accordingly.
    """

    def __init__(self, timestamp: datetime, configuration: Configuration):
        """
        Initialize the receive weight event.
        Args:
            configuration: The simulation configuration
        """
        super().__init__(timestamp, configuration)

    def fire(self, environment: Environment) -> List[Event]:
        super().log_event()
        # Compute the total weight by max train car capacity times the passenger mean weight
        max_weight = self.configuration.train_capacity * self.configuration.passenger_mean_weight
        # Get the light thresholds from the configuration, which we will use
        # to compute what color the light should be.
        thresholds = self.configuration.station_light_thresholds
        # The yellow threshold is below 75% of the max weight
        yellow_threshold = max_weight * thresholds['yellow']
        # The green threshold is below 50% of the max weight
        green_threshold = max_weight * thresholds['green']
        # Store the sector index where the train is going to be parked
        environment.train.parked_at = self.__decide_where_to_park(environment)

        # Now we loop through all the sectors and test the weight threshold of each car
        # and then light each station sector light accordingly.
        for i, sector in enumerate(environment.station.sectors):
            # We are only interested in the station sectors where there is a door.
            # Otherwise we will just continue.
            if i < environment.train.parked_at:
                continue
            if i > environment.train.parked_at + environment.train.train_car_length:
                break

            # Get the train car at the current sector. We minus by the index where the train is parked,
            # because if the train is parked at index 3, then the i=3 and therefore get train car number 3.
            # By subtracting the parked_at index, then we get train car 0, 1 and so forth.
            # We can do this because of the security checks above.
            train_car = environment.train[i - environment.train.parked_at]
            weight = train_car.weight

            # Light the sector lights accordingly.
            if weight <= green_threshold:
                ReceiveWeightEvent.__set_light_status(sector.sector_index, LightStatus.GREEN, environment)
            elif weight <= yellow_threshold:
                ReceiveWeightEvent.__set_light_status(sector.sector_index, LightStatus.YELLOW, environment)
            else:
                ReceiveWeightEvent.__set_light_status(sector.sector_index, LightStatus.RED, environment)
        return {PassengerDecisionEvent(self.timestamp + datetime.timedelta(seconds= + self.configuration.time_passenger_decision_event), self.configuration)}

    @staticmethod
    def __set_light_status(index: int, status: LightStatus, environment: Environment) -> None:
        """
        Set the light at the index to the provided light status
        Args:
            index: The index of the light
            status: The new light status
            environment: The environment the light exists in
        """
        environment.station.sectors[index].light.status = status

    def __decide_where_to_park(self, environment: Environment) -> int:
        """
        Decide which station sector index to park the train
        Args:
            environment: The simulation environment
        Returns: The sector index where the first door of the train should be parked.
        """

        # If the configuration says where to park, then we will park the train there
        if self.configuration.train_park_at_index is not None and self.configuration.train_park_at_index >= 0:
            return self.configuration.train_park_at_index

        # Otherwise we try to figure out where to park the train.
        # First, if the train is shorter than the amount of station sectors, then we get the difference
        # between the amount of sectors and choose a random number between 0 and the missing length.
        # For example, if the train is 10 cars long and there are 16 sectors, then the train can be parked
        # between sector index 0 and 6. This is chosen randomly and if we want to specify the same sector each time,
        # then we must do that using the configuration.
        if environment.train.train_car_length < self.configuration.station_sector_count:
            train_length_under_station = self.configuration.station_sector_count - environment.train.train_car_length
            return random_between_range(range(0, train_length_under_station))

        # If we for some reason have a train that is longer than the amount of sectors on the station,
        # let us get notified so that all the passengers have the ability to get off.
        if environment.train.train_car_length > self.configuration.station_sector_count:
            raise EnvironmentError("The train is longer than the platform and therefore will not fit.")

        # This means that the only option we have left is the possibility of the train being the length of the
        # platform and the train must therefore stop all the way at the end.
        return 0
