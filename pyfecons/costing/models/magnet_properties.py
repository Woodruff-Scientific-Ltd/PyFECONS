from dataclasses import dataclass

from pyfecons.inputs.magnet import Magnet
from pyfecons.units import Meters3, Meters2, Turns, Amperes, MA, Kilometers, AmperesMillimeters2, Meters, M_USD, Kilograms


@dataclass
class MagnetProperties:
    # input
    magnet: Magnet = None

    # computed
    vol_coil: Meters3 = None  # volume of the coil
    cs_area: Meters2 = None  # cross-sectional area of entire coil
    turns_c: Turns = None  # turns of cable in the coil
    cable_current: Amperes = None  # current per cable
    current_supply: MA = None  # total current supply to the coil
    turns_sc_tot: Turns = None  # total turns of REBCO
    turns_scs: Turns = None  # turns of REBCO in one cable
    tape_length: Kilometers = None  # total length of REBCO in km
    turns_i: Turns = None  # turns of (partial?) insulation
    j_tape: AmperesMillimeters2 = None  # approximate critical current density
    cable_w: Meters = None  # Cable width in meters
    cable_h: Meters = None  # Cable height in meters
    # number of pancakes based on total required turns and the number of turns in a reference pancake coil
    no_p: float = None
    vol_i: Meters3 = None  # total volume of insulation
    max_tape_current: Amperes = None  # current
    cost_sc: M_USD = None  # total cost of REBCO
    cost_cu: M_USD = None  # total cost of copper
    cost_ss: M_USD = None  # total cost of stainless steel
    cost_i: M_USD = None  # total cost of insulation
    coil_mass: Kilograms = None  # mass of the coil
    cooling_cost: M_USD = None
    tot_mat_cost: M_USD = None
    magnet_cost: M_USD = None
    magnet_struct_cost: M_USD = None
    magnet_total_cost_individual: M_USD = None
    magnet_total_cost: M_USD = None
    cu_wire_current: Amperes = None  # current through each cu_wire
