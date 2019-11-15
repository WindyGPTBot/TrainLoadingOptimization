from Runtimes.Configuration import Configuration
from Runtimes.Parameters import Parameters
from Runtimes.Environment import Environment
from Runtimes.EventRunTime import EventRunTime
from Runtimes.RunTime import RunTime


class ApplicationRunTime(RunTime):
    """
    Class that represents the overall application runtime.
    This includes both the GUI and the event chain.
    """

    def __init__(self, options: dict, params: dict):
        """
        Initialize a new application runtime
        """
        self.configuration = Configuration(options)
        self.parameters = Parameters(params)
        self.environment = Environment(self.configuration, self.parameters)

    def run(self) -> None:
        # Run the events
        event_runtime = EventRunTime(self.configuration, self.environment)
        event_runtime.run()

