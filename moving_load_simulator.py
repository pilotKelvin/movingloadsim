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
# disable()

getcontext().prec = 2


class MovingLoadSimulator:
    def __init__(self, beam_length, moving_interval, axle_positions):
        """
        :param beam_length:
        :param moving_interval:
        :param axle_positions:
        """
        self.beam_length = beam_length
        self.moving_interval = moving_interval
        self.axle_positions = axle_positions

        self.fn_simulate_moving_vehicle(self.beam_length, self.moving_interval, self.axle_positions)

    def fn_simulate_moving_vehicle(self, beam_length_: float, moving_interval_: float, axle_positions_: list) -> np:
        """
        This function generates position of each axle along the beam as the vehicle move
        :param beam_length_:
        :param moving_interval_:
        :param axle_positions_:
        :return axle_location_arr:
        """
        # generates points along the beam at the moving interval provided
        steps_to_move_arr = np.append(np.arange(0, beam_length_, moving_interval_), self.beam_length)
        # get the number of points generated
        no_of_steps_to_move = steps_to_move_arr.size
        # initialize an empty array to store axle locations later
        # Each row stores axle positions for point_x. No. of rows are equal to points generated
        axle_locations_arr = np.empty([no_of_steps_to_move, len(axle_positions_)], dtype=float)

        # find axle positions of each point generated
        for index, point_x in enumerate(steps_to_move_arr):
            axle_locations_arr[index][
                0] = point_x  # any point_x along the beam is always the location of the first axle
            for index_, axle_position in enumerate(axle_positions_):
                if axle_position == 0:  # first axle position coincides with point_x
                    pass
                else:
                    position = round(point_x - axle_position,
                                     2)  # compute each axle position in relation to point_x except for first axle
                    axle_locations_arr[index][index_] = position  # append each axle position to axle_location_arr.
                    # Each row of the axle_location_arr represents axle positions for point_x

        # compute influence lines
        influence_ordinates_arr = axle_locations_arr.copy()  # make a copy of axle locations
        influence_ordinates_arr = (
                                              beam_length_ - influence_ordinates_arr) / beam_length_  # compute influence line ordinates
        influence_ordinates_arr[influence_ordinates_arr > 1] = 0  # filter out values greater than one
        # round off values in the influence ordinate array. Use for loop to round values in each row since round takes 1 D array
        for index, row in enumerate(influence_ordinates_arr):
            influence_ordinates_arr[index] = np.round(row, 2)

        debug(f"{axle_locations_arr.ndim}")
        debug("********************")
        debug(f"{influence_ordinates_arr.ndim}")

        return axle_locations_arr  # return numpy array with all axle positions at each point along the beam


if __name__ == '__main__':
    # supply testing inputs
    beam_length = 30
    moving_interval = 0.5
    axle_positions = [0, 1.2]

    simulator = MovingLoadSimulator(beam_length, moving_interval, axle_positions)

# Next assignment - Tue 03/08/2021
# 1. Refactor self.fn_simulate_moving_vehicle() especially output data type. Consider Series or dataFrame as output
# 2. Add comments
# 3. Test with more data. Prepare example data output to be checked by Spencer
# 4. Return value

