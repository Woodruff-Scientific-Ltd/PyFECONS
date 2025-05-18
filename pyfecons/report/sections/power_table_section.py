from dataclasses import dataclass
from typing import Dict, Any

from pyfecons.report.section import ReportSection
from pyfecons.costing.accounting.power_table import PowerTable
from pyfecons.inputs.basic import Basic
from pyfecons.inputs.power_input import PowerInput
from pyfecons.enums import ReactorType


@dataclass
class PowerTableSection(ReportSection):
    """Report section for power table data."""

    def __init__(self, power_table: PowerTable, basic: Basic, power_input: PowerInput):
        super().__init__()

        if basic.reactor_type == ReactorType.MFE:  # MFE
            self.template_file = "powerTableMFEDT.tex"
            self.replacements = {
                # Ordered by occurrence in template
                # 1. Output power
                "PNRL": basic.p_nrl,  # Fusion Power
                "PALPHA": power_table.p_alpha,  # Alpha Power
                "PNEUTRON": power_table.p_neutron,  # Neutron Power
                "MN___": power_input.mn,  # Neutron Energy Multiplier
                "ETAP__": power_input.eta_p,  # Pumping power capture efficiency
                "PTH___": power_table.p_th,  # Thermal Power
                "ETATH": power_input.eta_th,  # Thermal conversion efficiency
                "PET___": power_table.p_et,  # Total (Gross) Electric Power
                # 2. Recirculating power
                "PLOSS": power_table.p_loss,  # Lost Power
                "PCOILS": power_table.p_coils,  # Power into coils
                "PTF___": power_input.p_tf,  # Power into TF coils
                "PPF___": power_input.p_pf,  # Power into PF (equilibrium) coils
                "FPCPPF": power_input.fpcppf,  # Primary Coolant Pumping Power Fraction
                "PPUMP": power_table.p_pump,  # Primary Coolant Pumping Power
                "FSUB": power_input.f_sub,  # Subsystem and Control Fraction
                "PSUB": power_table.p_sub,  # Subsystem and Control Power
                "PAUX": power_table.p_aux,  # Auxiliary systems
                "PTRIT": power_input.p_trit,  # Tritium Systems
                "PHOUSE": power_input.p_house,  # Housekeeping power
                "PCOOL": power_table.p_cool,  # Cooling systems
                "PTFCOOL": power_input.p_tfcool,  # TF coil cooling
                "PPFCOOL": power_input.p_pfcool,  # PF coil cooling
                "PCRYO": power_input.p_cryo,  # Cryo vacuum pumping
                "ETAPIN": power_input.eta_pin,  # Input power wall plug efficiency
                "PINPUT": power_input.p_input,  # Input power
                # 3. Outputs
                "QSCI": power_table.q_sci,  # Scientific Q
                "QENG": power_table.q_eng,  # Engineering Q
                "RECFRAC": round(
                    power_table.rec_frac, 3
                ),  # Recirculating power fraction
                "PNET": power_table.p_net,  # Output Power (Net Electric Power)
            }
        elif basic.reactor_type == ReactorType.IFE:
            self.template_file = "powerTableIFEDT.tex"
            self.replacements = {
                "PNRL": round(basic.p_nrl, 1),
                "PALPHA": round(power_table.p_alpha, 1),
                "PNEUTRON": round(power_table.p_neutron, 1),
                "MN": round(power_input.mn, 1),
                "FPCPPF": round(power_input.fpcppf, 1),
                "FSUB": round(power_input.f_sub, 1),
                "PTRIT": round(power_input.p_trit, 1),
                "PHOUSE": round(power_input.p_house, 1),
                "PAUX": round(power_table.p_aux, 1),
                "PCRYO": round(power_input.p_cryo, 1),
                "ETAPIN1": round(power_input.eta_pin1, 1),
                "ETAPIN2": round(power_input.eta_pin2, 1),
                "ETAP": round(power_input.eta_p, 1),
                "ETATH": round(power_input.eta_th, 1),
                "PIMPLOSION": round(power_input.p_implosion, 1),
                "PIGNITION": round(power_input.p_ignition, 1),
                "PTH": round(power_table.p_th, 1),
                "PET": round(power_table.p_et, 1),
                "PLOSS": round(power_table.p_loss, 1),
                "GAINE": round(power_table.gain_e, 1),
                "PTARGET": round(power_input.p_target, 1),
                "PMACHINERY": round(power_input.p_machinery, 1),
                "PSUB": round(power_table.p_sub, 1),
                "QS": round(power_table.q_sci, 1),
                "QE": round(power_table.q_eng, 1),
                "EPSILON": round(power_table.rec_frac, 1),
                "PNET": round(power_table.p_net, 1),
                "PP": round(power_table.p_pump, 1),
                "PIN": round(power_input.p_input, 1),
            }
        else:
            raise ValueError(f"Unknown reactor type: {basic.reactor_type}")
