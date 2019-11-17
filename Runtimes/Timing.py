from datetime import datetime


class Timing:
    """
    Class to hold timing data like turn around time
    """

    def __init__(self):
        self.__start_time: datetime = None
        self.__stop_time: datetime = None

    @property
    def turn_around_time(self) -> float:
        """
        Get the turn around time
        Returns: The turn around time in seconds
        """
        # Safety None checks
        if self.__start_time is None:
            raise RuntimeError("You must start the timer before getting the turn around time")
        if self.__stop_time is None:
            raise RuntimeError("You must stop the timer before getting the turn around time")
        # Get the time difference between the stop and start timers
        diff = self.__stop_time - self.__start_time
        # Get the total difference in seconds
        return diff.total_seconds()

    def start_timer(self, start_time: datetime) -> None:
        """
        Start the turn around timer
        Args:
            start_time: The time where the turn around starts
        """
        self.__start_time = start_time

    def stop_timer(self, stop_time: datetime) -> None:
        """
        Stop the turn around timer
        Args:
            stop_time: The time where the simulation stops
        """
        if self.__start_time is None:
            raise RuntimeError("You should start the timer before stopping it")

        self.__stop_time = stop_time
