from typing import Dict, List, Union

from Distributions.Distribution import Distribution


class Configuration:
    """
    This class represents all the configuration/options for the simulation components and more
    """

    def __init__(self, options: Dict):
        """
        Initialize the configuration
        Args:
            options: A dictionary containing all the options
        """
        self.__options = options

    @property
    def passenger_weight_distribution(self) -> Distribution:
        """
        Get the range which passenger weights should be created
        Returns:
            A range object with the passenger minimum and maximum weight
        """
        return self.__options['passenger_weight_distribution']

    @property
    def passenger_mean_weight(self) -> float:
        """
        Get the passenger mean weight.
        This option is made to compute the maximum mean weight that a train car can carry.
        Returns: The passenger mean weight
        """
        return self.__options['passenger_mean_weight']

    @property
    def passenger_speed_range(self) -> range:
        """
        Get the range which passenger speed should be created
        Returns:
            A range object with the passenger minimum and maximum speed
        """
        return self.__options['passenger_speed_range']

    @property
    def passenger_loading_time_range(self) -> range:
        """
        Get the range which passenger loading time should be set
        Returns:
            A range object with the passenger minimum and maximum loading time
        """
        return self.__options['passenger_loading_time_range']

    @property
    def passenger_regular_size(self) -> float:
        """
        Get the regular passenger size
        Returns:
            The regular passenger size as a float
        """
        return self.__options['passenger_regular_size']

    @property
    def passenger_max_walk_range(self) -> range:
        """
        Get the range which passengers will maximum walk
        Returns:
            A range object with the passenger minimum and maximum range
        """
        return self.__options['passenger_max_walk_range']

    @property
    def passenger_compliance(self) -> float:
        """
        Get the percentage for how compliant the passenger will be.
        Returns:
            A float as percentage with 0 for never compliant and 1 for always compliant.
        """
        return self.__options['passenger_compliance']

    @property
    def station_sector_count(self) -> int:
        """
        Get the amount of sectors that a station have
        Returns: The amount of sectors a station should have
        """
        return self.__options['station_sector_count']

    @property
    def station_stairs_placement(self) -> List[int]:
        """
        Get the amount of stairs for the station creation
        Returns:
            An int with the amount of stairs to be created
        """
        return self.__options['station_stairs_placement']

    @property
    def station_sector_passenger_max_count(self) -> int:
        """
        Get the maximum number of passengers that can fit into a single station sector
        Returns:
            An integer for the maximum number of passengers that can fit in a single station sector
        """
        return self.__options['station_sector_passenger_max_count']

    @property
    def station_sector_fullness(self) -> range:
        """
        Get a percentage of how full the station sectors should be. The fullness is represented as a range object,
        so that we can choose to populate the station sectors randomly between a certain amount.
        Returns: A range of how full the station sector should be populated.
        """
        return self.__options['station_sector_fullness']

    @property
    def station_stair_factor(self) -> float:
        """
        Get the factor of how much the distance to the stairs should factor in,
        when we populate the station with passengers.
        Returns:
            The station factor of how much stairs matter in populating stations.
        """
        return self.__options['station_stair_factor']

    @property
    def station_light_thresholds(self) -> Dict[str, float]:
        """
        Get the different thresholds that will tell us what light the different
        lights should be based on the weight of the train car that will stop there.
        Returns:
            At dictionary with **green** and **yellow** that holds a float for
            how much beneath the max weight of the train car that color should be lit.
        """
        return self.__options['station_light_thresholds']

    @property
    def train_fullness(self) -> range:
        """
        Get a percentage of how full the trains should be. The fullness is represented as a range object,
        so that we can choose to populate the train cars randomly between a certain amount.
        Returns: A range of how full the train should be populated.
        """
        return self.__options['train_fullness']

    @property
    def train_unload_percent(self) -> range:
        """
        Get a range of percentages for how much each car should unload at the station.
        Returns: A range object between 0 and 100 with how much each car should be unloaded.
        """
        return self.__options['train_unload_percent']

    @property
    def train_set_setup(self) -> int:
        """
        Get the amount of cars that a train set consists of.
        Returns: The amount of cars in a train set
        """
        return self.__options['train_set_setup']

    @property
    def train_amount_of_sets(self) -> int:
        """
        Get the amount of train sets to be spawned for the train
        Returns: The amount of train sets
        """
        return self.__options['train_amount_of_sets']

    @property
    def train_park_at_index(self) -> Union[int, None]:
        """
        Get the station sector index where the train will stop with its first door.
        Returns: None if the train should decide automatically, or the station sector index
        """
        return self.__options['train_park_at_index']

    @property
    def train_capacity(self) -> int:
        """
        Get the amount of passengers that will fit in a train car
        Returns: The max train car capacity
        """
        return self.__options['train_capacity']

    @property
    def time_arrive_event(self) -> float:
        return self.__options['time_arrive_event']

    @property
    def time_depart_event(self) -> float:
        return self.__options['time_depart_event']

    @property
    def time_load_passenger_event(self) -> float:
        return self.__options['time_load_passenger_event']

    @property
    def time_unload_passenger_event(self) -> float:
        return self.__options['time_unload_passenger_event']

    @property
    def time_passenger_decision_event(self) -> float:
        return self.__options['time_passenger_decision_event']

    @property
    def time_receive_weight_event(self) -> float:
        return self.__options['time_receive_weight_event']

    @property
    def time_send_weight_event(self) -> float:
        return self.__options['time_send_weight_event']

    @property
    def time_weigh_train_event(self) -> float:
        return self.__options['time_weigh_train_event']

    def __str__(self):
        """
        Override the string representation to display the dictionary
        Returns:
            The options dictionary string representation
        """
        return str(self.__options)

