import unittest
import Main
from Runtimes import ApplicationRuntime


class TestReceivedWeightEvent(unittest.TestCase):
    """
    A class to test received weight events.
    """

    def setUp(self) -> None:
        self.options = Main.options
        self.runtime = ApplicationRuntime.ApplicationRunTime(self.options)

    def test_station_lights(self):
        """
        Test whether the non-marginal station sectors have light.
        """
        for sector in self.runtime.environment.station.sectors:
            if sector.train_car:
                self.assertIsNotNone(sector.light.status)
            else:
                self.assertIsNone(sector.light.status)

    def test_station_has_passengers(self):
        """
            At least one of the station sectors has passengers.
        """
        sectors = self.runtime.environment.station.sectors
        has_pas = False

        for sector in sectors:
            if sector.amount > 1:
                has_pas = True

        self.assertTrue(has_pas)


    def test_number_of_passengers_at_station(self):
        """
            Test if the amount of passengers in the station is as
            expected.
        """

        self.options['environment_random_seed'] = 30
        self.options['station_sector_fullness'] = range(100, 100)
        self.options['station_sector_passenger_max_count'] = 20
        self.options['station_stair_factor'] = 3
        self.options['station_stairs_placement'] = [5, 8]
        self.runtime = ApplicationRuntime.ApplicationRunTime(self.options)

        sectors = self.runtime.environment.station.sectors
        expected_passengers = [5, 8, 11, 14, 17, 20, 17, 17, 20, 17, 14, 11, 8, 5, 2, 0]
        # All sectors must have the same amount of passengers every time the test runs
        for sector in sectors:
            self.assertEqual(expected_passengers[sector.sector_index], sector.amount)
        print("Number of passengers in sections is as expected")

    def test_number_of_passengers_at_stair_sector(self):
        """
            Test if the Number of passengers at a stair section is always the maximum capacity of passengers.
        """

        self.options['environment_random_seed'] = 30
        self.options['station_sector_fullness'] = range(100, 100)
        self.options['station_sector_passenger_max_count'] = 20
        self.options['station_stair_factor'] = 3
        # every sector has a stair
        self.options['station_stairs_placement'] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        self.runtime = ApplicationRuntime.ApplicationRunTime(self.options)

        sectors = self.runtime.environment.station.sectors
        expected_passengers = [20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20]
        # All sectors must have the same max amount of passengers every time the test runs
        for sector in sectors:
            self.assertEqual(expected_passengers[sector.sector_index], sector.amount)
        print("Number of passengers at a stair section is always the maximum capacity of passengers")

    def tearDown(self) -> None:
        pass
