from abc import ABC, abstractmethod


class RunTime(ABC):
    """
    Abstract class that represent a longer running process or application runtime.
    """

    @abstractmethod
    def run(self) -> None:
        """
        Start the runtime
        """
        raise NotImplementedError("Run method has not been implemented")
