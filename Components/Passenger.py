import random

from Components.Component import Component
from Helpers.Ranges import random_between_range
from Runtimes.Configuration import Configuration
from uuid import UUID, uuid4


class Passenger(Component):
    """
    This class represents a passenger that will be on the station or in the train.
    """

    def __init__(self, configuration: Configuration):
        """
        Initialize a new passenger component
        """
        self.id: UUID = uuid4()
        self.speed = random_between_range(configuration.environment_random_seed, configuration.passenger_speed_range)
        self.loading_time = random_between_range(configuration.environment_random_seed, configuration.passenger_loading_time_range)
        self.weight = configuration.passenger_weight_distribution.generate_single()
        self.size = configuration.passenger_regular_size
        self.max_walk = random_between_range(configuration.environment_random_seed, configuration.passenger_max_walk_range)
        super().__init__(configuration)

    def __str__(self):
        return "Passenger (s: {}, lt: {}, w: {}, sz: {}, mw: {})".format(
            self.speed, self.loading_time, self.weight, self.size, self.max_walk)

    def is_compliant(self) -> bool:
        random.seed(self.configuration.environment_random_seed)
        return random.random() <= self.configuration.passenger_compliance
