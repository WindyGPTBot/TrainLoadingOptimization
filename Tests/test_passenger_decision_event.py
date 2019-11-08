import unittest

from Distributions.NormalDistribution import NormalDistribution
from Runtimes import ApplicationRuntime
from Events.PassengerDecisionEvent import PassengerDecisionEvent
from Helpers import DateTime
from datetime import datetime


class TestPassengerDecisionEvent(unittest.TestCase):
    """
    A class to test passenger events.
    """

    def setUp(self) -> None:
        self.options: dict = {
            "passenger_weight_distribution": NormalDistribution(80, 10),
            "passenger_mean_weight": 80,
            "passenger_speed_range": range(5, 10),
            "passenger_loading_time_range": range(1, 3),
            "passenger_regular_size": 0.5,
            "passenger_max_walk_range": range(0, 6),
            "passenger_compliance": 0.8,
            "train_capacity": 75,
            "train_fullness": range(40, 80),
            "train_unload_percent": range(30, 50),
            "train_set_setup": 4,
            "train_amount_of_sets": 2,
            "train_park_at_index": None,
            "station_sector_count": 16,
            "station_distance": 3.0,
            "station_stairs_placement": [3],
            "station_sector_passenger_max_count": 25,
            "station_sector_fullness": range(20, 50),
            "station_stair_factor": 1.5,
            "station_light_thresholds": {"green": .5, "yellow": .75},
            "time_arrive_event": 60,
            "time_depart_event": 0,
            "time_load_passenger_event": 1,
            "time_unload_passenger_event": 1,
            "time_passenger_decision_event": 5,
            "time_receive_weight_event": 10,
            "time_send_weight_event": 0,
            "time_weigh_train_event": 3,
            "time_door_action": 4
        }
        self.runtime = ApplicationRuntime.ApplicationRunTime(self.options)

    def test_passenger_move_upon_red_light(self):
        self.options['train_capacity'] = 70
        env = self.runtime.environment
        conf = self.runtime.environment.configuration
        station = self.runtime.environment.station
        car = self.runtime.environment.train.train_sets[0].cars[0]
        car.add(passengers=70 - car.amount, configuration=conf)
        print(station.sectors[0].has_train_car())

        # We make this car full
        print('', )

        now = datetime.now()
        p_event_1 = PassengerDecisionEvent(
            now,
            DateTime.add_seconds(now, 0),
            self.runtime.configuration
        )




    def tearDown(self) -> None:
        pass
