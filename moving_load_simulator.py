"""
Module name: moving_load_simulator.py
Purpose: Simulate a vehicle moving over a simply supported beam
Author: Kelvin Macharia W
Year: August 2021.
"""

from decimal import Decimal, getcontext
from logging import basicConfig, DEBUG, debug,disable
from sys import argv
import pprint

basicConfig(level= DEBUG, format=' %(message)s')
disable()

getcontext().prec = 2

class MovingLoadSimulator():
    def __init__(self, beam_length, moving_interval, axle_positions):
        """
        Instantiates instant variables and formats self.results() which is the class output
        :param beam_length:
        :param moving_interval:
        :param axle_positions:
        """
        self.beam_length = beam_length
        self.moving_interval = moving_interval
        self.axle_positions = axle_positions

        # dictionary to store the output of this class
        self.simulation_data = {}
        # Format of the result dictionary will be as follows:
        '''
        {
        step:{
                'axle_distances': [ ... ]
                'ordinates': [ ... ]
             }
             
             }
             ...
             }
             ...
        }
        '''
        # construct results dictionary
        axles_location_dict = self.fn_simulate_moving_vehicle() # generate distances
        axles_influence_ordinates_dict = self.fn_point_load_ordinates() # generate influence lines

        for axle_position in axles_location_dict.keys():
            min_dict = {}
            min_dict["axle_distances"] = axles_location_dict[axle_position]
            min_dict["ordinates"] = axles_influence_ordinates_dict[axle_position]
            # print(axle_position)
            self.simulation_data[axle_position] = min_dict

    def fn_simulate_moving_vehicle(self):
        '''
        Simulates movement of a vehicle over a simply supported beam.
        (At the moment the program allows the car to move forward. Effect on reversing especially for SV 196 and SOV should be explored.)
        Moves the vehicle at the intervals specified/provided and then generate positions for axle in relation to first support.
        inputs: self.beam_length, self.vehicle_axle_positions, self.moving_interval
        :return: axles_locations_dict # stores axle positions at each step the vehicle moves
        '''
        self.steps_to_move = round((self.beam_length / self.moving_interval) + 1) # determine how many steps of the interval specified the vehicle moves
        debug(f"No.of {self.moving_interval} metres steps moved = {self.steps_to_move }")
        cumulative_vehicle_movement = 0 # Accumulating variable for vehicle steps/intervals. Accumulates each step after every loop

        axles_location_dict = {} # dict to store position of all axle at each step
        for step in range(self.steps_to_move): # loop through the determined step
            x_distances = [] # clear list beginning of each step to store new axle locations
            for position in self.axle_positions: # for every step find location of each axle in relation to first support
                axle_position = round((cumulative_vehicle_movement - position),2)
                x_distances.append(axle_position) # append each axle location in a list

            axles_location_dict[step+1] = x_distances # add list of axle position for each step to axle location dict
            cumulative_vehicle_movement += self.moving_interval # move vehicle to next position

        return axles_location_dict # return dic with all axle positions at each step

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

        return axles_influence_ordinates_dict # return dict with influence ordinates

if __name__ == '__main__':
    # supply testing inputs

    beam_length = 30
    moving_interval = 0.5
    axle_positions = [0, 1.2,2.4,3.6,4.8,6]

    simulator = MovingLoadSimulator(beam_length, moving_interval, axle_positions)

    pprint.pprint(simulator.simulation_data)

# Next assignment - Done 05/04/2021
# 1. Test generation of special vehicle influence ordinate
     # Testing outcome
        #  improve fn_simulate_moving_vehicle() to generate position of all axle in rlt to first support

# Next task - Done 06/04/2021
# 1. Improve fn_simulate_moving_vehicle() to generate position of all axle in relation to first support and repeat testing for LM1, LM2 and LM3
# 2. Update fn_point_load_ordinates() for changes in task 1
# 3. Improve the storage of influence ordinates
# 4. Research on best data structure for storing lots of data

# Next task - Done 08/05/2021
# 1. Test
# 2. Refactor
# 3. More documentation


