"""
Module name: moving_load_simulator.py
Purpose: Simulate a vehicle moving over a simply supported beam
Author: Kelvin Macharia W
Year: August 2021
"""
from decimal import Decimal, getcontext
from logging import basicConfig, DEBUG, debug, disable
from sys import argv
import pprint

import numpy as np
import pandas as pd
import sympy as sp

basicConfig(level=DEBUG, format=' %(message)s')
disable()
# pandas settings to display all data
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

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
        :return axle_locations_pdsr, influence_ordinates_pdsr:
        """
        # generates points along the beam at the moving interval provided
        xpoints_along_beam = np.append(np.arange(0, beam_length_, moving_interval_), self.beam_length)
        # get the number of points generate d
        no_of_xpoints = xpoints_along_beam.size
        # initialize an empty array to store axle locations later
        # Each row stores axle positions for point_x. No. of rows are equal to points generated
        axle_locations_arr = np.empty([no_of_xpoints, len(axle_positions_)], dtype=float)

        # find axle positions of each point generated
        for index, point_x in enumerate(xpoints_along_beam):
            positions = np.round(point_x - axle_positions, 2)  # compute each axle position in relation to point_x except for first axle
            axle_locations_arr[index] = positions  # append each axle position to axle_location_arr.

        # compute influence lines
        influence_ordinates_arr = axle_locations_arr.copy()  # make a copy of axle locations
        influence_ordinates_arr = np.round(((beam_length_ - influence_ordinates_arr) / beam_length_), decimals=2)
        influence_ordinates_arr[influence_ordinates_arr > 1] = 0  # filter out values greater than one
        # convert outputs to pandas Series
        axle_locations_pdsr = pd.Series(axle_locations_arr.tolist(), index=[ind + 1 for ind in range(no_of_xpoints)])
        influence_ordinates_pdsr = pd.Series(influence_ordinates_arr.tolist(), index=[ind + 1 for ind in range(no_of_xpoints)])

        debug(axle_locations_pdsr)
        debug("------------------------")
        debug(influence_ordinates_pdsr)

        return axle_locations_pdsr, influence_ordinates_pdsr  # return 2 pandas Series with all axle positions and influence ordinates at each point along the beam

# self test code
if __name__ == '__main__':
    # supply testing inputs
    beam_length = 30
    moving_interval = 0.1
    axle_positions = [0, 1.2, 2.4, 3.6, 4.8, 6.0]

    sim_data = MovingLoadSimulator()(beam_length, moving_interval, axle_positions)
    print(sim_data)

# Next assignment

