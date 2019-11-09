import unittest
import Main
from Runtimes import ApplicationRuntime


class TestPrepareTrainEvent(unittest.TestCase):
    """
    A class to test train events.
    """

    def setUp(self) -> None:
        self.options = Main.options
        self.runtime = ApplicationRuntime.ApplicationRunTime(self.options)

    def test_train_leaves_full(self):
        """
        After running the simulation, we must make sure the train has left full.
        """
        self.options['simulation_random_seed'] = 30
        self.options['station_sector_fullness'] = range(100, 100)
        self.options['station_sector_passenger_max_count'] = 25
        self.options['train_capacity'] = 20
        self.options['train_set_setup'] = 1  # Amount of cars
        self.options['train_amount_of_sets'] = 2  # Amount of sets
        self.options['train_fullness'] = range(100, 100)

        self.runtime.run()
        train_sets = self.runtime.environment.train.train_sets
        # All cars must be full
        for set in train_sets:
            for car in set.cars:
                self.assertTrue(car.is_full())
