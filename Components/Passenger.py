from Components.Component import Component
from Runtimes.Configuration import Configuration
from Helpers.Ranges import random_between_range
from random import random

class Passenger(Component):
    """
    This class represents a passenger that will be on the station or in the train.
    """

    def __init__(self, configuration: Configuration):
        """
        Initialize a new passenger component
        """
        self.speed = random_between_range(configuration.passenger_speed_range)
        self.loading_time = random_between_range(configuration.passenger_loading_time_range)
        self.weight = configuration.passenger_weight_distribution.generate_single()
        self.size = configuration.passenger_regular_size
        self.max_walk = random_between_range(configuration.passenger_max_walk_range)
        super().__init__(configuration)

    def __str__(self):
        return "Passenger (s: {}, lt: {}, w: {}, sz: {}, mw: {})"\
            .format(self.speed, self.loading_time, self.weight, self.size, self.max_walk)

    def is_compliant(self) -> bool:
        return random() >= self.configuration.passenger_compliance
