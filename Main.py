from Distributions.NormalDistribution import NormalDistribution
from Runtimes.ApplicationRuntime import ApplicationRunTime


if __name__ == '__main__':
    options: dict = {
        "passenger_weight_distribution": NormalDistribution(80, 10),
        "passenger_mean_weight": 80,
        "passenger_speed_range": range(1, 3),
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
        "station_stairs_placement": [3],
        "station_sector_passenger_max_count": 25,
        "station_sector_fullness": range(20, 50),
        "station_stair_factor": 1.5,
        "station_light_thresholds": {"green": .5, "yellow": .75}
    }

    # Run the application
    application = ApplicationRunTime(options)
    application.run()
