from Events.Event import Event
from Runtimes.Configuration import Configuration
from Runtimes.Environment import Environment


class WeighTrainEvent(Event):
    """
    Event when the train gets weighed.
    The train is weighed by summing all the passenger weights together
    """
    def __init__(self, configuration: Configuration):
        super().__init__(configuration)

    def fire(self, environment: Environment) -> None:
        # Adding all the passengers weights together
        # and storing it in the train weight property
        for train_set in environment.train.train_sets:
            for train_car in train_set.cars:
                for passenger in train_car.passengers:
                    train_car.weight += passenger.weight
                environment.train.weight += train_car.weight
