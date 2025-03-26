from pyfecons.costing.ife.cas22.nif_costs import (
    get_nif_scaled_costs,
    get_nif_replacements,
)
from pyfecons.costing.categories.cas220103_lasers import CAS220103Lasers
from pyfecons.inputs.lasers import Lasers
from pyfecons.inputs.power_input import PowerInput


def cas_220103_laser_costs(power_input: PowerInput, lasers: Lasers) -> CAS220103Lasers:
    # Cost Category 22.1.3: Lasers
    cas220103 = CAS220103Lasers()

    scaled_costs = get_nif_scaled_costs(power_input.p_implosion, lasers)
    replacements = get_nif_replacements(scaled_costs)

    cas220103.C220103 = scaled_costs["22.1.3. Laser"].total
    replacements["C220103"] = str(round(cas220103.C220103))

    cas220103.template_file = "CAS220103_IFE_DT.tex"
    cas220103.replacements = replacements
    return cas220103
