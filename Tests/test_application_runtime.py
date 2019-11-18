import unittest
import Main
from Runtimes import ApplicationRuntime


class TestPassengerDecisionEvent(unittest.TestCase):
    """
    A class to test passenger events.
    """

    def setUp(self) -> None:
        self.options = Main.options
        self.runtime = ApplicationRuntime.ApplicationRunTime(self.options)


    def test_can_start_runtime(self):
        """
        Test if the application runtime can be started.
        """
        self.assertIsNone(self.runtime.run())

    def tearDown(self) -> None:
        pass
