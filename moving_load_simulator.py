"""
Module name: moving_load_simulator.py
Purpose: Simulate a vehicle moving over a simply supported beam
Author: Kelvin Macharia W
Year: August 2021
"""

from decimal import Decimal, getcontext
from logging import basicConfig, DEBUG, debug,disable
from sys import argv
import pprint

import numpy as np
import pandas as pd
import sympy as sp

basicConfig(level= DEBUG, format=' %(message)s')
# disable()

getcontext().prec = 2

class MovingLoadSimulator():
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

    def fn_simulate_moving_vehicle(self, beam_length, moving_interval, axle_positions):
        """
        This function generates position of each axle along the beam as the vehicle move
        :param beam_length:
        :param moving_interval:
        :param axle_positions:
        :return: axle_location_arr
        """
        steps_to_move_arr = np.append(np.arange(0, self.beam_length, self.moving_interval), self.beam_length) # generates points along the beam with moving interval provided
        no_of_steps_to_move = steps_to_move_arr.size # get the number of points generated

        axle_location_arr = np.empty([no_of_steps_to_move, len(axle_positions)], dtype=float) # initialize an empty to populate with axle location later

        for index, point in enumerate(steps_to_move_arr): # find axle positions of each point generated
            axle_location_arr[index][0] = point
            for index_, axle in enumerate(axle_positions):
                if axle == 0:
                    pass
                else:
                    position = round(point - axle, 2)
                    axle_location_arr[index][index_] = position

        debug(f"{axle_location_arr}")

        return axle_location_arr # return numpy array with all axle positions at each point along the beam

    def fn_point_load_ordinates(self):
        '''
        calculates ordinates of each axle position at each step the vehicle moves
        inputs: self.beam_length, axles_location_dict
        :return: influence_ordinates_dict # stores influence ordinates of every axle at each step the vehicle moves
        '''
        axles_location_dict = self.fn_simulate_moving_vehicle()

        axles_influence_ordinates_dict = {}

        for step in axles_location_dict.keys():
            ordinates_lst = []
            # debug(x_distances_dict[step])
            for axle_position in axles_location_dict[step]: # loop
                if axle_position < 0:
                    ordinates_lst.append(0)
                    # influence_ordinates[step+1] = ordinates
                else:
                    distance_from_far_support = self.beam_length - axle_position
                    ordinate = round(((1 / self.beam_length) * distance_from_far_support),2)  # compute ordinates and append to list
                    if ordinate < 0: # No ordinates should be negative. Due to round off steps moved. The first axle may move past the other other end giving a negative ordinates.
                        ordinate = 0.0
                    ordinates_lst.append(ordinate)
                axles_influence_ordinates_dict[step] = ordinates_lst

        return axles_influence_ordinates_dict  # return dict with influence ordinates

if __name__ == '__main__':
    # supply testing inputs
    beam_length = 30
    moving_interval = 0.5
    axle_positions = [0, 1.2, 2.4, 3.6, 4.8, 6.0]

    simulator = MovingLoadSimulator(beam_length, moving_interval, axle_positions)


# Next assignment - Tue 03/08/2021
# 1. Refactor self.fn_simulate_moving_vehicle() especially output data type. Consider Series or dataFrame as output
# 2. See if the two functions in this class can be merged


