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
        name = 'environment.pickle'
        p.save(name, self.environment)

        self.configuration.station_have_lights = False

        tas = {'with': 0, 'without': 0}

        # Run the events x times
        event_runtime = EventRunTime(self.configuration, p.read(name))
        event_runtime.run()
        tas['without'] += event_runtime.environment.timings.turn_around_time

        self.configuration.station_have_lights = True

        # Run the events x times
        event_runtime = EventRunTime(self.configuration, p.read(name))
        event_runtime.run()
        tas['with'] += event_runtime.environment.timings.turn_around_time

        print('with: {}, without: {}'.format(tas['with'], tas['without']))
