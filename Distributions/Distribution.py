from abc import ABC, abstractmethod
from typing import List, Union


class Distribution(ABC):
    """
    Abstract class that all distributions must inherit from
    """

    def fill(self, size: int = None, arr: list = None) -> List[float]:
        """
        Fill a list of the provided size or fill a list with the sampled distribution.
        Args:
            size: If provided, will generate a list of this size and fill it with the sampled distribution
            arr: If provided, will fill the list with the sampled distribution

        Returns:
            A list filled with the sampled distribution
        """
        if list is None and arr is None:
            raise TypeError("You must provide either a size of the list you want or a list to fill")

        # Let us generate a list of the provided size
        # and fill it with the distribution
        if size is not None:
            return self.generate_series(size)

        # If the size is None, then we must fill the provided list
        # First we generate a series with the size of the provided array
        distribution: List[float] = self.generate_series(len(arr))
        # Then we fill the array with the generated distribution
        for i in range(len(arr)):
            arr[i] = distribution[i]
        return arr

    @abstractmethod
    def generate_single(self) -> float:
        """
        Generate a single sample from the distribution
        Returns:
            A sample from the distribution
        """
        raise NotImplementedError("generate_single method not implemented in " + self.__class__.__name__)

    @abstractmethod
    def generate_series(self, size: int) -> List[float]:
        """
        Generate a series of the provided size from the distribution.
        Provides the same functionality as fill with the size provided
        Args:
            size:
                The size of the series to produce
        Returns:
            A series from the distribution
        """
        raise NotImplementedError("generate_series method not implemented in " + self.__class__.__name__)
