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
        pass
