class Timing:
    """
    Class to hold timing data like turn around time
    """

    def __init__(self):
        self.__turn_around = 0

    @property
    def turn_around(self):
        """
        Get the turn around time
        Returns: The turn around time
        """
        return self.__turn_around

    def add_ta_time(self, time: float) -> None:
        """
        Add the amount of time to the turn around time
        Args:
            time: The amount of time to add. Must be greater than 0.
        """
        if time < 0:
            raise TypeError("You can not reduce time")
        self.__turn_around += time

