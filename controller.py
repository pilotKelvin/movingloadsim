from decimal import Decimal, getcontext
from logging import basicConfig, DEBUG, debug
from pprint import pprint

from vehicle_data import vehicle_data_class as vdc
from moving_load_simulator import MovingLoadSimulator as mls

basicConfig(level= DEBUG, format=' %(message)s')

getcontext().prec = 2

class Controller:
    def __init__(self, vehicle_name, critical_distance, beam_length, moving_interval):
        # get vehicle data from vehicle class
        vehicle = vdc(vehicle_name, critical_distance)
        self.vehicle_data = vehicle.vehicle_data

        simulator = mls(beam_length, moving_interval, self.vehicle_data.axle_positions)
        self.simulation_data = simulator.simulation_data_namedtuple

    def __str__(self):
        return "controller class"

if __name__ == "__main__":
    controller = Controller("lm1", 0, 30, 1.0) # Controller(vehicle_name, critical_distance, beam_length, moving_interval)

    # pprint(controller.vehicle_data)
    pprint(controller.simulation_data)

# test with controller class