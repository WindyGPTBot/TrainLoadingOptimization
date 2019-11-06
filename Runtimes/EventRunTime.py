from datetime import datetime
from logging import getLogger

from Events.WeighTrainEvent import WeighTrainEvent
from Runtimes.Configuration import Configuration
from Runtimes.Environment import Environment
from Runtimes.EventQueue import EventQueue
from Runtimes.RunTime import RunTime


class EventRunTime(RunTime):
    """
    Class that is in charge of the event runtime.
    This means that the whole event chain will be run here.
    """

    def __init__(self, configuration: Configuration, environment: Environment):
        """
        Initialize the event runtime with the provided configuration and environment
        Args:
            configuration: The runtime configuration
            environment: The runtime environment
        """
        self.environment = environment
        self.configuration = configuration
        self.event_queue = EventQueue()
        self.logger = getLogger(self.__class__.__name__)

    def run(self) -> None:
        # Enqueue starting event
        self.event_queue.events.append(WeighTrainEvent(datetime.now(), self.configuration))

        # Execute events until none are left
        while len(self.event_queue.events) > 0:
            try:
                self.event_queue.events.extend(self.event_queue.get_next().run(self.environment))
            except RuntimeError as e:
                self.logger.warning(e)
