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
        self.runtime.run()
        for sector in self.runtime.environment.station.sectors:
            if sector.train_car:
                self.assertIsNotNone(sector.light.status)
            else:
                self.assertIsNone(sector.light.status)

    def test_station_has_passengers(self):
        pass

    def tearDown(self) -> None:
        pass
