from typing import List, Union

from Components.Passenger import Passenger
from Runtimes.Configuration import Configuration


class PassengerContainer:
    """
    Class that makes it possible to handle passengers.
    """

    def __init__(self):
        """
        Initialize the passenger container. Defaults to an empty container.
        """
        self.__passengers = []

    @property
    def amount(self) -> int:
        """
        Get the amount of passengers in this container
        Returns:
            The amount of passengers in the container
        """
        return len(self.__passengers)

    @property
    def passengers(self) -> List[Passenger]:
        """
        Get the list of passengers that live inside this container
        Returns:
            :rtype: list[Passenger] The list of passengers
        """
        return self.__passengers

    def add(self, passengers: Union[int, Passenger, List[Passenger]], configuration: Configuration = None) -> None:
        """
        Add the provided amount of passengers
        Args:
            passengers: If provided as an integer, the integer will represent the amount of passengers that will be added.
                If provided as a passenger, the passenger provided will simply be appended to the list.
                If provided as a list of passengers, the list will be concatenated with the existing list of passengers
                in the container.
            configuration: The configuration for which they will be spawned with. Must be provided if the **amount** is
                an integer.
        Raises:
            TypeError: Thrown if you provide invalid arguments. You must provide the configuration if passengers is an
                integer. Otherwise you provide a Passenger object or a list of Passenger objects.
        """
        if isinstance(passengers, int) and configuration is not None:
            for i in range(passengers):
                self.__passengers.append(Passenger(configuration))
        elif isinstance(passengers, Passenger):
            self.__passengers.append(passengers)
        elif isinstance(passengers, list):
            self.__passengers.extend(passengers)
        else:
            raise TypeError("You must provide valid passengers and configuration arguments.")

    def remove(self, amount: int = 1) -> List[Passenger]:
        """
        Pop the provided amount from the passenger container.
        You can not remove more than there are in the container.
        Args:
            amount: The amount to pop from the container
        Returns: A list of the passengers that was removed
        """
        passengers = []
        try:
            for i in range(amount):
                passenger = self.passengers.pop(0)
                passengers.append(passenger)
        except IndexError:
            pass
        finally:
            return passengers
