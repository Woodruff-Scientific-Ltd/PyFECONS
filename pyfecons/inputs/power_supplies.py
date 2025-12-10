from dataclasses import dataclass

from pyfecons.units import USD_W, K, Ratio, Unknown, V


@dataclass
class PowerSupplies:
    learning_credit: Ratio = None
    cost_per_watt: USD_W = None
    p_compress: Unknown = None
    cap_temp: K = None  # max temp rating of the film capacitor
    cap_temp_ambient: K = None  # ambient temperature of the application
    cap_temp_delta: K = None  # temperature rise due to ripple current
    cap_voltage: V = None  # rated voltage of capacitor
    cap_l1: Unknown = None  # load life rating of the film capacitor
