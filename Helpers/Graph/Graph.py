from abc import ABC, abstractmethod
from Runtimes.ApplicationRuntime import ApplicationRunTime
from typing import List
from Helpers.Object import get_deep_attr, has_deep_attr
from datetime import datetime

try:
    import matplotlib.pyplot as plt
    import numpy as np
except ImportError as e:
    raise BaseException('matplotlib could not be imported. Make sure it is properly installed. %s' % e)


class Graph(ABC):
    def __init__(
            self,
            samples: List[ApplicationRunTime],
            x_param: str,
            y_param: str,
            comparison_param: str,
            *args,
            **kwargs
    ):
        """

        Args:
            samples: Runtime samples
            x_param: Attribute to be extracted from runtime, i.e: runtime.environment.train.arrival_time
            y_param: Attribute to be extracted from runtime, i.e: runtime.environment.train.arrival_time
            comparison_param: Attribute to be extracted from runtime, i.e: runtime.environment.train.arrival_time
            *args:
            **kwargs:
        """
        self.samples = samples
        self.comparison_param = comparison_param
        self.y_param = y_param
        self.x_param = x_param

        # Optional arguments
        self.file_format = kwargs.get('file_format', 'svg').replace('.', '')
        self.file_name = kwargs.get('file_name', self.__class__.__name__.lower())
        self.title = kwargs.get('title', 'Result')

        # ...
        self.axes = {}

    @abstractmethod
    def compile_data(self) -> None:
        """
        Arranges the data to plot the graph.
        """
        raise NotImplementedError("Method not implemented in {}".format(self.__class__.__name__))

    @abstractmethod
    def draw(self) -> None:
        """
        Plots the graph and saves it to a file.
        """
        raise NotImplementedError("Method not implemented in {}".format(self.__class__.__name__))


class DictGraph(Graph):

    def __init__(
            self,
            samples: List[ApplicationRunTime],
            x_param: str,
            y_param: str,
            comparison_param: str,
            *args,
            **kwargs):
        self.without_lights = []
        self.with_lights = []
        super().__init__(samples, x_param, y_param, comparison_param, args, kwargs)

    def compile_data(self) -> None:
        for sample in self.samples:
            self.without_lights.append(sample.without_lights)
            self.with_lights.append(sample.with_lights)

    def draw(self) -> None:
        self.compile_data()
        plt.plot(self.without_lights)
        plt.plot(self.with_lights)
        plt.legend(['Without Lights', 'With Lights'], loc='upper left')
        plt.ylabel('Turn around time')
        plt.xlabel('Configuration')
        plt.savefig('graph.svg')
        plt.savefig('graph.png')
        plt.show()


class SimpleGraph(Graph):
    def compile_data(self) -> None:
        """
        Prepares the data to be graphed.
        """

        for i, r in enumerate(self.samples):
            # Get the parameters from the objects

            if has_deep_attr(r, self.y_param):
                y_value = get_deep_attr(r, self.y_param)
            else:
                raise Exception('y_param attribute does not exist.')

            if has_deep_attr(r, self.x_param):
                x_value = get_deep_attr(r, self.x_param)
            else:
                raise Exception('x_param attribute does not exist.')

            if has_deep_attr(r, self.comparison_param):
                comparison_value = get_deep_attr(r, self.comparison_param)
            else:
                raise Exception('comparison_value attribute does not exist.')

            # If comparison values have different values across all simulations,
            # two graphs will be plotted together. That is why we have a list of axes (x, y), one
            # for each dictionary key.

            # Name for the key in the dictionary
            key = '%s=%s' % (self.comparison_param, comparison_value)

            try:
                # Append to the X and Y axes for this parameter

                # Keys do exist
                self.axes[key][0].append(x_value)
                self.axes[key][1].append(y_value)
            except KeyError:
                # Keys do not exist
                self.axes[key] = [[x_value], [y_value]]

    def draw(self):
        """
        Plots graph.
        """
        # Gets the data
        self.compile_data()

        # For each comparison parameter, we get the axis Y and X
        for key, v_axes in self.axes.items():
            # Sorting the values in asc order
            v_axes[0].sort(), v_axes[1].sort()
            # Plots
            plt.plot(v_axes[0], v_axes[1], label=key)

        # Naming the axes
        plt.xlabel(self.x_param)
        plt.ylabel(self.y_param)

        plt.title(self.title)
        plt.legend()
        plt.grid(True)

        # Unique name for the figure
        _stamp = datetime.now().strftime('%Y%m%d%H%M%S')
        plt.savefig('%s-%s.%s' % (
            self.file_name,
            _stamp,
            self.file_format
        ))
        plt.show()
