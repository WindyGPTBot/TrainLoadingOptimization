import json
import logging.config
import pickle

from Distributions.NormalDistribution import NormalDistribution
from Runtimes.ApplicationRuntime import ApplicationRunTime
from Runtimes.Environment import Environment

options: dict = {
    "passenger_weight_distribution": NormalDistribution(80, 10),
    "passenger_mean_weight": 80,
    "passenger_speed_range": range(10, 10),
    "passenger_loading_time_range": range(4, 4),
    "passenger_regular_size": 0.5,
    "passenger_max_walk_range": range(4, 4),
    "passenger_compliance": 1,
    "train_capacity": 75,
    "train_fullness": range(30, 60),
    "train_unload_percent": range(30, 50),
    "train_set_setup": 4,
    "train_amount_of_sets": 2,
    "train_park_at_index": None,
    "station_sector_count": 16,
    "station_distance": 1.0,
    "station_stairs_placement": [3],
    "station_sector_passenger_max_count": 25,
    "station_sector_fullness": range(30, 60),
    "station_stair_factor": 1.5,
    "station_light_thresholds": {"green": .5, "yellow": .75},
    "station_have_lights": True,
    "time_send_weight_event": 0,
    "time_receive_weight_event": 0,
    "time_door_action": 4,
    "environment_random_seed": None,
}

if __name__ == '__main__':

    # Create the logger configuration from the json file
    with open('logging.json', 'rt') as f:
        config = json.load(f)
    logging.config.dictConfig(config)

    # Run the application

    application = ApplicationRunTime(options)
    application.run()
