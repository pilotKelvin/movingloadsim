"""
Module name: moving_load_simulator.py
Purpose: Simulate a vehicle moving over a simply supported beam
Author: Kelvin Macharia W
Year: August 2021
"""
import logging
from collections import namedtuple
import numpy as np

logging.basicConfig(level=logging.INFO, format=' %(message)s')
# disable()

class MovingLoadSimulator:
    def __call__(self, beam_length: float, moving_interval: float, axle_positions: list):
        """
        :param beam_length:
        :param moving_interval:
        :param axle_positions:
        """
        self.beam_length = beam_length
        self.moving_interval = moving_interval
        self.axle_positions = np.array(axle_positions)

        self.sim_data = self.fn_simulate_moving_vehicle(self.beam_length, self.moving_interval, self.axle_positions)

        return self.sim_data

    def fn_simulate_moving_vehicle(self, beam_length_: float, moving_interval_: float, axle_positions_: np) -> np:
        """
        This function generates position of each axle along the beam as the vehicle move
        :param beam_length_:
        :param moving_interval_:
        :param axle_positions_:
        :return simulation_data:
        """
        # Generate points along the beam at the moving interval provided
        x_coordinates_along_beam = np.arange(0, beam_length_+moving_interval_, moving_interval_)
        # get the number of points generate d
        no_of_xpoints = x_coordinates_along_beam.size
        # initialize an empty array to store axle locations later
        # Each row stores axle positions for point_x. No. of rows are equal to point generated
        axle_locations_arr = np.empty([no_of_xpoints, len(axle_positions_)], dtype=float)

        # find axle positions of each point generated
        for index, point_x in enumerate(x_coordinates_along_beam):
            positions = np.round(point_x - axle_positions_, 2)  # compute each axle position in relation to point_x except for first axle
            axle_locations_arr[index] = positions  # append each axle position to axle_location_arr

        # compute influence lines
        influence_ordinates_arr = axle_locations_arr.copy()  # make a copy of axle locations
        influence_ordinates_arr = np.round(((beam_length_ - influence_ordinates_arr) / beam_length_), decimals=2) # (L - x)/L
        influence_ordinates_arr[influence_ordinates_arr > 1] = 0  # filter out values greater than 1
        # store the two array outputs in a named tuple for ease of retrieval
        simulation_data = namedtuple("simulation_data", ["axle_locations_arr", "influence_ordinates_arr"])
        simulation_data = simulation_data(axle_locations_arr, influence_ordinates_arr)

        return simulation_data  # return a tuple of 2 named tuple

# self test code
if __name__ == '__main__':
    # supply testing inputs
    beam_length = 30
    moving_interval = 1.0
    axle_positions = [0, 1.2, 2.4, 3.6, 4.8, 6.0]

    simulation_data = MovingLoadSimulator()(beam_length, moving_interval, axle_positions)
    logging.info(simulation_data)


