#!/usr/bin/python3

"""
Module name: vehicle_data.py
Purpose: Generate vehicle data
Author: Kelvin Macharia
Year: 2021
"""

from logging import basicConfig, DEBUG, debug, disable
from sys import argv
from pprint import pprint
from collections import namedtuple

basicConfig(level= DEBUG, format=' %(message)s')
disable()

class vehicle_data_class:
    """
    vehicle data class. Contains or settings/properties for all load models and vehicles.
    """

    def __call__(self, vehicle_type, critical_distance = None):
        """
        Object of this class is called as a function and returns vehicle data
        :param vehicle_name:
        :param critical_distance: # this is a kwarg therefore optional. Only special vehicles have this parameter
        :return: vehicle_data
        """
        vehicle_data = self.get_vehicle_data(vehicle_type, critical_distance) # call self.get_vehicle_data to generate vehicle data requested
        return vehicle_data

    def get_vehicle_data(self, vehicle_type, critical_distance):
        """
        Generates data for vehicle type requested by self.__init__().
        :param vehicle_type:
        :param critical_distance:
        :return: vehicle_data # named tuple data type
        """
        # variable to handle error
        error_message = None

        # create a named tuple to store vehicle data
        vehicle_data = namedtuple("vehicle_data",
                                  ["vehicle_type", "number_of_axles", "axle_positions", "axle_spacing",
                                   "vehicle_length", "standard_axle_loads", "udl", "units"])

        if vehicle_type.upper() == "LM1":
            vehicle_type = "LM1"
            axle_number = 2
            axle_positions = [0, 1.2]
            axle_spacings = {"s1": 1.2}
            vehicle_length = 1.2
            standard_axle_loads = {"NL1": [300, 300], "NL2": [100, 100], "NL3": [50, 50], "RA": [0, 0]}  # standard axle load as in Eurocodes & UK N.A
            standard_udl = {"NL1": 5.49, "NL2": 5.50, "NL3": 5.50, "RA": 5.50}

        elif vehicle_type.upper() == "LM2":
            vehicle_type = "LM2"
            axle_number = 0
            axle_positions = [0]
            axle_spacings = {}
            vehicle_length = 0
            standard_axle_loads = {"NL": [400]}  # standard axle load as in Eurocodes & UK N.A
            standard_udl = 0

        if vehicle_type.upper() == "SV80" or vehicle_type.upper() == "SV100":
            try:
                assert critical_distance == 1.2 or critical_distance == 5.0 or critical_distance == 9.0, \
                    str(critical_distance) + " is not a valid critical distance for " + str(vehicle_type)

                axle_number = 6
                axle_positions = [0, 1.2, 2.4,
                                       round((2.4 + critical_distance), 2),
                                       round((2.4 + critical_distance + 1.2), 2),
                                       round((2.4 + critical_distance + 1.2 + 1.2), 2)]
                axle_spacings = {"s1": 1.2, "s2": 1.2, "s3": float(critical_distance), "s4": 1.2, "s5": 1.2}
                vehicle_length = axle_positions[-1]

                if vehicle_type.upper() == "SV80":
                    vehicle_type = "LM3_SV80"
                    standard_axle_loads = {"NL": [130, 130, 130, 130, 130, 130]}  # standard axle load as in Eurocodes & UK N.A

                elif vehicle_type.upper() == "SV100":
                    vehicle_type = "LM3_SV100"
                    standard_axle_loads = {"NL": [165, 165, 165, 165, 165, 165]} # standard axle load as in Eurocodes & UK N.A

                standard_udl = 0

            except AssertionError as error:
                error_message = error
                return error_message

        elif vehicle_type.upper() == "SV196":
            try:
                assert critical_distance == 1.2 or critical_distance == 5.0 or critical_distance == 9.0, \
                    str(critical_distance) + " is not a valid critical distance for " + str(vehicle_type)

                vehicle_type = "LM3_SV196"
                axle_number = 12
                axle_positions = [0, 4.4, 6.0, 10, 11.2, 12.4, 13.6,
                                       round((13.6 + critical_distance), 2),
                                       round((13.6 + critical_distance + 1.2), 2),
                                       round((13.6 + critical_distance + 1.2 + 1.2), 2),
                                       round((13.6 + critical_distance + 1.2 + 1.2 + 1.2), 2),
                                       round((13.6 + critical_distance + 1.2 + 1.2 + 1.2 + 1.2), 2)
                                       ]
                axle_spacings = {"s1": 4.4, "s2": 1.6, "s3": 4.0, "s4": 1.2, "s5": 1.2, "s6": 1.2,
                                     "s7": float(critical_distance), "s8": 1.2, "s9": 1.2, "s10": 1.2, "s11": 1.2}
                vehicle_length = axle_positions[-1]
                standard_axle_loads = {"NL":[165, 165, 165, 165, 165, 165, 165, 165, 165, 180, 180,
                                            100]}  # standard axle load as in Eurocodes & UK N.A
                standard_udl = 0

            except AssertionError as error:
                error_message = error
                return error_message

        if error_message == None:
            units = {"linear": "m", "point_loads": "kN", "udl": "kN/m\u00b2"}

            vehicle_data = vehicle_data(vehicle_type, axle_number, axle_positions, axle_spacings, vehicle_length, standard_axle_loads, standard_udl, units)

            return vehicle_data  # return named tuple containing vehicle data requested


if __name__ == "__main__":
    if len(argv) > 1:
        # run from command line
        vehicle_data = vehicle_data_class()(str(argv[1]), float(argv[2]))
        pprint(vehicle_data['vehicle_type'])
        pass
    else:
        vehicle_data = vehicle_data_class()("lm1")
        pprint(vehicle_data)

# Next task - Done on 08/05/2021
#