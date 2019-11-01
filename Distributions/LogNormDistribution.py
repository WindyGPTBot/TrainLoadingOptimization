from typing import List

from numpy.random import lognormal

from Distributions.Distribution import Distribution


class LogNormDistribution(Distribution):
    """
    Logarithmic normal distribution
    """

    def __init__(self, mean: float, sigma: float):
        """
        Initialize a new Log Normal Distribution
        Args:
            mean: Mean value of the underlying normal distribution
            sigma: Standard deviation of the underlying normal distribution. Should be greater than zero.
        """
        self.__mean = mean
        self.__sigma = sigma

    def generate_single(self) -> float:
        return lognormal(self.__mean, self.__sigma, 1)

    def generate_series(self, size: int) -> List[float]:
        return lognormal(self.__mean, self.__sigma, size)

