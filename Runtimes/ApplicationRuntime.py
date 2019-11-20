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
        self.with_lights = 0
        self.without_lights = 0

    def run(self) -> None:
        name = 'environment.pickle'
        p.save(name, self.environment)

        self.configuration.station_have_lights = False

        event_runtime = EventRunTime(self.configuration, p.read(name))
        event_runtime.run()
        self.without_lights = event_runtime.environment.timings.turn_around_time

        self.configuration.station_have_lights = True

        # Run the events x times
        event_runtime = EventRunTime(self.configuration, p.read(name))
        event_runtime.run()
        self.with_lights = event_runtime.environment.timings.turn_around_time
