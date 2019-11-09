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
            At least one of the train sectors has passengers.
        """
        sectors = self.runtime.environment.station.sectors
        has_pas = False

        for sector in sectors:
            if sector.amount > 1:
                self.assertTrue(has_pas)


    def tearDown(self) -> None:
        pass
