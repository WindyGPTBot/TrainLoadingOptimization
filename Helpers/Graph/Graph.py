from abc import ABC, abstractmethod
from Runtimes.ApplicationRuntime import ApplicationRunTime
from typing import List

try:
    import matplotlib.pyplot as plt
    import numpy as np
except ImportError as e:
    raise BaseException('matplotlib could not be imported. Make sure it is properly installed. %s' % e)

class Graph(ABC):
    def __init__(self, runtime : List[ApplicationRunTime], comparison_parameter : str, *args, **kwargs):
        """
        Initializes a class to plot graphs based on the passed runtime.
        Args:
            runtime: the runtime object
            *args:
            **kwargs: file_Format, file_name, title
        """
        self.runtime = runtime
        self.comparison_parameter = comparison_parameter

        # Optional arguments
        self.file_format = kwargs.get('file_format', 'svg').replace('.', '')
        self.file_name = kwargs.get('file_name', self.__class__.__name__.lower())
        self.title = kwargs.get('title', 'Result')

        # ...
        self.x_axis = kwargs.get('x_axis', [])
        self.y_axis = {}

    @abstractmethod
    def build_data(self) -> None:
        """
        Arranges the data to plot the graph.
        """
        raise NotImplementedError("method not implemented in {}".format(self.__class__.__name__))

    @abstractmethod
    def draw(self) -> None:
        """
        Plots the graph and saves it to a file.
        """
        raise NotImplementedError("method not implemented in {}".format(self.__class__.__name__))


class SimpleGraph(Graph):
    def build_data(self):

        for i, r in enumerate(self.runtime):
            # Adds this value to the corresponding key
            key = getattr(r.environment.configuration, self.comparison_parameter)
            value = r.environment.timings.turn_around_time

            try:
                self.y_axis[key].append(value)
            except KeyError:
                self.y_axis[key] = []
                self.y_axis[key].append(value)

        # Since the X axis has to be the same for all Y axis, we make sure to sample only once, as this list grows
        # linearly with the different amount of parameters n*m
        for i, r in enumerate(self.runtime):
            self.x_axis.append(
                r.environment.station.amount_passengers(follow_through=False)
            ) if not (i % len(self.y_axis) and self.x_axis) else None

    def draw(self):
        self.build_data()
        for key, items in self.y_axis.items():
            plt.plot(self.x_axis, items, label='%s=%s' % (self.comparison_parameter, key))

        plt.xlabel('passengers on platform')
        plt.ylabel('turn around time')

        plt.title(self.title)
        plt.legend()
        plt.grid(True)
        plt.savefig('%s.%s' % (self.file_name, self.file_format))
        plt.show()
