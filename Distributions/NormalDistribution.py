from typing import List

from Distributions.Distribution import Distribution
from numpy.random import normal


class NormalDistribution(Distribution):
    """
    Normal distribution
    """

    def __init__(self, mean: float, scale: float = 1):
        """
        Initialize a new normal distribution
        Args:
            mean: The mean (center) of the normal distribution
            scale: Standard deviation (spread or "width") of the normal distribution
        """
        self.__mean = mean
        self.__scale = scale

    def generate_single(self) -> float:
        return normal(self.__mean, self.__scale)

    def generate_series(self, size) -> List[float]:
        return normal(self.__mean, self.__scale, size)
