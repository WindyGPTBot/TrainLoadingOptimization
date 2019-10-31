from Events.ReceiveWeightEvent import ReceiveWeightEvent
from Events.WeighTrainEvent import WeighTrainEvent
from Runtimes.Configuration import Configuration
from Runtimes.Environment import Environment
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

    def run(self) -> None:
        # First we weigh the train at the departing station
        departing_loading = WeighTrainEvent(self.configuration)
        departing_loading.fire(self.environment)

        # Then we receive the weight information at the arriving station
        receive_weight_info = ReceiveWeightEvent(self.configuration)
        receive_weight_info.fire(self.environment)