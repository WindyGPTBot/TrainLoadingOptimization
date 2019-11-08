import Main
import unittest
from Runtimes import ApplicationRuntime
from Events.PassengerDecisionEvent import PassengerDecisionEvent
from Helpers import DateTime
from datetime import datetime


class TestPassengerDecisionEvent(unittest.TestCase):
    """
    A class to test passenger events.
    """

    def setUp(self) -> None:
        self.options = Main.options
        self.runtime = ApplicationRuntime.ApplicationRunTime(self.options)

    def test_passenger_move_upon_red_light(self):
        pass


    def tearDown(self) -> None:
        pass
