import datetime

from Events.ReceiveWeightEvent import ReceiveWeightEvent
from Events.WeighTrainEvent import WeighTrainEvent
from Runtimes.Configuration import Configuration
from Runtimes.Environment import Environment
from Runtimes.RunTime import RunTime
from EventQueue import  EventQueue


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
        self.eventqueue = EventQueue()

    def run(self) -> None:
        #Encqueue starting event
        self.eventqueue.events.append(WeighTrainEvent(datetime.datetime.now(), self.configuration))

        #Execute events until none are left
        while len(self.eventqueue.events) > 0:
            self.eventqueue.events.extend(self.eventqueue.get_next().fire(self.environment))

#        # First we weigh the train at the departing station
#        departing_loading = WeighTrainEvent(self.configuration)
#        departing_loading.fire(self.environment)
#
#        # Then we receive the weight information at the arriving station
#        receive_weight_info = ReceiveWeightEvent(self.configuration)
#        receive_weight_info.fire(self.environment)
