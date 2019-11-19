import json
import logging.config

from Distributions.NormalDistribution import NormalDistribution
from Runtimes.ApplicationRuntime import ApplicationRunTime

options: dict = {
    "passenger_weight_distribution": NormalDistribution(80, 10),
    "passenger_mean_weight": 80,
    "passenger_speed_range": range(5, 5),
    "passenger_loading_time_range": range(4, 4),
    "passenger_regular_size": 0.5,
    "passenger_max_walk_range": range(4, 4),
    "passenger_compliance": 1,
    "train_capacity": 75,
    "train_fullness": range(30, 60),
    "train_unload_percent": range(10, 50),
    "train_set_setup": 4,
    "train_amount_of_sets": 2,
    "train_park_at_index": 8,
    "station_sector_count": 16,
    "station_distance": 3.0,
    "station_stairs_placement": [3],
    "station_sector_passenger_max_count": 25,
    "station_sector_fullness": range(50, 80),
    "station_stair_factor": 1.5,
    "station_light_thresholds": {"green": .5, "yellow": .75},
    "station_have_lights": True,
    "time_send_weight_event": 0,
    "time_receive_weight_event": 0,
    "time_door_action": 4,
    "environment_random_seed": 30,
}

if __name__ == '__main__':

    # Create the logger configuration from the json file
    with open('logging.json', 'rt') as f:
        config = json.load(f)
    logging.config.dictConfig(config)
    #@TODO remove
    logging.disable()

    # Run the application
    changes = {'time_send_weight_event': [0, 1, 2]}

    samples = []

    for i in range(20,60):
        for key, values in changes.items():
            for value in values:
                opt = options
                print(options)
                opt[key] = value
                print(opt)
                application = ApplicationRunTime(opt)
                application.run()
                samples.append(application)

    from Helpers.Graph.Graph import SimpleGraph
    s_graph = SimpleGraph(samples, comparison_parameter='time_send_weight_event')
    s_graph.draw()
