from dataclasses import dataclass
from pyfecons.report import TemplateProvider
from pyfecons.units import MW, Unknown, Ratio


@dataclass
class PowerTable(TemplateProvider):
    p_alpha: MW = None  # Charged particle power
    p_neutron: MW = None  # Neutron power
    p_cool: MW = None
    p_aux: MW = None  # Auxiliary systems
    p_coils: MW = None
    p_th: MW = None  # Thermal power
    p_the: MW = None  # Total thermal electric power
    p_dee: MW = None
    p_et: MW = None  # Total (Gross) Electric Power
    p_loss: MW = None  # Lost Power
    p_pump: MW = None  # Primary Coolant Pumping Power
    p_sub: MW = None  # Subsystem and Control Power
    q_sci: Unknown = None  # Scientific Q
    q_eng: Unknown = None  # Engineering Q
    rec_frac: Unknown = None  # Recirculating power fraction
    p_net: MW = None  # Output Power (Net Electric Power)
    gain_e: Ratio = None  # Gain in Electric Power
