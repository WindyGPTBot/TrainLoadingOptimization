from typing import Optional

from Runtimes.Configuration import Configuration
from Runtimes.Environment import Environment
from Runtimes.EventRunTime import EventRunTime
from Runtimes.RunTime import RunTime
import Helpers.Pickle as p


class ApplicationRunTime(RunTime):
    """
    Class that represents the overall application runtime.
    This includes both the GUI and the event chain.
    """

    def __init__(self, options: dict, environment: Optional[Environment] = None):
        """
        Initialize a new application runtime
        """
        self.configuration = Configuration(options)
        self.environment = Environment(self.configuration) if environment is None else environment

    def run(self) -> None:
        event_runtime = EventRunTime(self.configuration, self.environment)
        event_runtime.run()
