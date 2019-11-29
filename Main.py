import sys, getopt
import json
import logging.config

from Distributions.NormalDistribution import NormalDistribution
from Runtimes.ApplicationRuntime import ApplicationRunTime
from Helpers.Graph.Graph import DictGraph

options: dict = {
    "passenger_weight_distribution": NormalDistribution(80, 10),
    "passenger_mean_weight": 80,
    "passenger_speed_range": range(5, 5),
    "passenger_loading_time_range": range(4, 4),
    "passenger_regular_size": 0.5,
    "passenger_max_walk_range": range(16, 16),
    "passenger_compliance": 1,
    "train_capacity": 100,
    "train_fullness": range(30, 60),
    "train_unload_percent": [30, 30, 30, 30, 30, 30, 30, 30],
    "train_set_setup": 4,
    "train_amount_of_sets": 2,
    "train_park_at_index": 8,
    "station_sector_count": 16,
    "station_distance": 3.0,
    "station_stairs_placement": [3, 14],
    "station_sector_passenger_max_count": 100,
    "station_sector_fullness": range(20, 30),
    "station_stair_factor": 1.5,
    "station_light_thresholds": {"green": .5, "yellow": .75},
    "station_have_lights": False,
    "time_send_weight_event": 0,
    "time_receive_weight_event": 0,
    "time_door_action": 4,
    "environment_random_seed": 30
}


def start_simulation(silence=False, plot=False):
    # Create the logger configuration from the json file
    with open('logging.json', 'rt') as f:
        config = json.load(f)
    logging.config.dictConfig(config)

    # Toggles logging
    logging.disable() if silence else None

    # Stores simulation examples
    samples = []

    # Possible combinations for the simulation
    plots = {
        'station_have_lights': [True, False]
    }

    changes = {
        'station_sector_passenger_max_count': [30, 50, 55, 60, 65, 70, 80, 85, 90]
    }

    # We run different simulations with the different parameters saved above
    # Here we modify the options. We plot different values for 'plots' together with 'changes'
    print("Running simulation...")

    for k, vls in plots.items():
        for v in vls:
            for key, values in changes.items():
                for value in values:
                    options[k] = v
                    options[key] = value
                    application = ApplicationRunTime(options)
                    application.run()
                    samples.append(application)

    print("Simulations finished.")

    if plot:
        print("Plotting graph...")
        s_graph = SimpleGraph(
            samples,
            # Values in X
            x_param='environment.station.initial_passenger_amount',
            # Values in Y
            y_param='environment.timings.turn_around_time',
            # Different plots if this value changes under the simulation (or before=
            comparison_param='configuration.station_have_lights')
        s_graph.draw()

    print("Finished!")


def introduction():
    PRESENTATION = """
    ###############################################################
    ##                                                           ##
    ##              TECHNICAL UNIVERSITY OF DENMARK              ##
    ##                                                           ##
    ##                     SIMULATION OF                         ##
    ## OPTIMIZATION DEVICE FOR PASSENGER LOADING IN TRAIN WAGONS ##
    ##          02223 - MODEL BASED SYSTEMS ENGINEERING          ##
    ##                                                           ##
    ##              LAURA GRÜNAUER & S191883                     ##
    ##              THOMAS MADSEN & S154174                      ##
    ##              ELVIS  CAMILO & S190395                      ##
    ##              DAVID SØRENSEN & S182862                     ##
    ##                                                           ##
    ##                    NOVEMBER 2019                          ##
    ###############################################################
    """

    # Credits https://www.asciiart.eu/vehicles/trains
    TRAIN = """
    ___________   _______________________________________^__.
     ___   ___ |||  ___   ___   ___    ___ ___  |   __  ,____|
    |   | |   |||| |   | |   | |   |  |   |   | |  |  | |_____|
    |___| |___|||| |___| |___| |___|  | O | O | |  |  |        )
               |||                    |___|___| |  |__|         )
    ___________|||______D_S_B___________________|______________/
               |||                                        /---------
    -----------'''---------------------------------------'
    ################################################################
    """

    print('{}{}'.format(PRESENTATION, TRAIN))


def usage():
    introduction()
    instructions = """
    Usage:
             -s, --silence  Toggles logging
             -p, --plot-graph  Draw a graph with the simulation result
    """
    print(instructions)


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], ":hsn", ["help"])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)

    silence = False
    plot_graph = True

    for o, a in opts:
        if o in ("-s", "--silence"):
            silence = True
        elif o in ("-n", "--no-plotting"):
            plot_graph = False
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        else:
            assert False, "unhandled option"

    # Starts simulation
    introduction()
    start_simulation(silence, plot_graph)
    sys.exit()


if __name__ == "__main__":
    main()
