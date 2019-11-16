from Runtimes.Configuration import Configuration
from Runtimes.Environment import Environment
from Runtimes.EventRunTime import EventRunTime
from Runtimes.RunTime import RunTime


class ApplicationRunTime(RunTime):
    """
    Class that represents the overall application runtime.
    This includes both the GUI and the event chain.
    """

    def __init__(self, options: dict):
        """
        Initialize a new application runtime
        """
        self.configuration = Configuration(options)
        self.environment = Environment(self.configuration)

    def run(self) -> None:
        # Run the events x times
        event_runtime = EventRunTime(self.configuration, self.environment)
        event_runtime.run()
