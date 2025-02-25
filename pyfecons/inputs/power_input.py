from dataclasses import dataclass
from pyfecons.units import Percent, MW, Ratio


@dataclass
class PowerInput:
    f_sub: Percent = None  # Subsystem and Control Fraction
    p_cryo: MW = None
    mn: Ratio = None  # Neutron energy multiplier
    eta_p: Percent = None  # Pumping power capture efficiency
    eta_th: Percent = None  # Thermal conversion efficiency
    fpcppf: Percent = None  # Primary Coolant Pumping Power Fraction
    p_trit: MW = None  # Tritium Systems
    p_house: MW = None  # Housekeeping power
    p_tfcool: MW = None  # Solenoid coil cooling
    p_pfcool: MW = None  # Mirror coil cooling
    p_tf: MW = None  # Power into TF coils
    p_pf: MW = None  # Power into PF (equilibrium) coils (TODO - how to handle for HTS?)
    eta_pin: Percent = None  # Input power wall plug efficiency
    eta_pin1: Percent = None
    eta_pin2: Percent = None
    eta_de: Percent = None  # Direct energy conversion efficiency
    p_input: MW = None  # Input power
    p_implosion: MW = None  # Implosion laser power
    p_ignition: MW = None  # Ignition laser power
    p_target: MW = None  # Power into target factory
    p_machinery: MW = None  # Power into machinery
