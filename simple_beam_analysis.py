#!/usr/bin/python3
"""
Module name: simple_beam_analysis.py
Purpose: Finds reactions, shear and moments as the vehicle over a simply supported beam.
       : Finds maximum moment and shear and the location they occur along the simply supported beam.
Author: Kelvin Macharia
Year: 2021
"""


from vehicle_data import vehicle_data_class as vdc
from moving_load_simulator import MovingLoadSimulator as mls

from logging import basicConfig, DEBUG, debug, disable
from sys import argv
from pprint import pprint



basicConfig(level= DEBUG, format=' %(message)s')
# disable()

class SimpleBeamAnalysis:
    def __init__(self):
        # get vehicle data from vehicle class
        vehicle_data = vdc()("lm1", 0)
        axle_loads = vehicle_data.standard_axle_loads["NL1"] # make it a user input later, for debugging just provide from vehicle data class
        axle_positions = vehicle_data.axle_positions

        # get simulation data i.e ordinates and axle distances
        simulator = mls(30, 1.0, axle_positions)
        simulation_data = simulator.simulation_data
        print(simulation_data)

        # axle and udl loads from variable action loads

        # create class variable


        # call class methods
        self.reactions = self.fn_calculate_reactions(axle_loads, simulation_data)
        self.moments = self.fn_calculate_moments()

    def fn_calculate_reactions(self, axle_loads: list ,simulation_data: dict(type='dict', help='simulation_data dict is nested, extract ordinates')) ->dict:
        # possible revision when the influence line concept is revised
        """
        Compute reactions i.e R1 & R2
        :param axle_loads:
        :param simulation_data:
        :param beam_length:
        :param udl:
        :return: reactions
        """
        reactions = {} # dictionary to store reactions
        # compute reaction due to udl

        for key in simulation_data.keys(): # access simulation data dict keys
            ordinates = simulation_data[key]['ordinates'] # for every key, retrieve ordinate list
            reaction_pair = {}# list to store reaction pair for each ordinates list
            R1 = 0
            sum = 0
            for i, ordinate in enumerate(ordinates): # retrieve every ordinate in the list and its index
                R1 = round((R1 + (ordinate * axle_loads[i])),2) # compute R1 by multiplying each ordinate with respective axle load in the axle load list
                if ordinate != 0 or key == len(simulation_data):
                    sum += axle_loads[i] # accumulate all axle loads whose ordinates are not zero and the last all axle loads when the vehicle reaches the last point

            R2 = sum - R1  # compute reaction R2 by subtracting R1 from summation of all axle
            reaction_pair['R1'] = R1 # append Reaction R1 to list
            reaction_pair['R2'] = R2 # append Reaction R2 to list
            reactions[key] = reaction_pair # add reaction pair to dictionary

        return reactions # return dictionary with reaction pairs for each point the vehicle move



    def fn_calculate_moments(self):
        # wait until revision of influence lines is done
        pass

sba = SimpleBeamAnalysis()
pprint(sba.reactions)
# pprint(sba.moments)

# Task
# 1. Finish refactoring fn_calculate_reactions() and document
# 2. Figure out how to store
# 3. Analysis with udl loading from P.A and VA
# 4. When load be factor or amplified with dynamic factors