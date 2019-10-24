from Components.Component import Component
from Components.LightStatus import LightStatus
from Runtimes.Configuration import Configuration


class Light(Component):
    """
    Traffic light component placed on the station to signal the passengers.
    """

    def __init__(self, configuration: Configuration, status: LightStatus = None):
        """
        Initialize a new light component
        Args:
            configuration: The component configuration
            status: Optional status of the station light. Will default to RED if not provided.
        """
        super().__init__(configuration)
        self.__status = status

    @property
    def status(self) -> LightStatus:
        """
        Get the light status

        Returns: The light status
        """
        return self.__status

    @status.setter
    def status(self, new_status: LightStatus) -> None:
        # We default to red if the light status is not provided or is provided as a wrong type
        if new_status is None:
            new_status = LightStatus.RED
        self.__status = new_status

