from pyfecons.costing.ife.cas22.nif_costs import (
    get_nif_scaled_costs,
)
from pyfecons.costing.categories.cas220103_lasers import CAS220103Lasers
from pyfecons.inputs.lasers import Lasers
from pyfecons.inputs.power_input import PowerInput


def cas_220103_laser_costs(power_input: PowerInput, lasers: Lasers) -> CAS220103Lasers:
    # Cost Category 22.1.3: Lasers
    cas220103 = CAS220103Lasers()

    scaled_costs = get_nif_scaled_costs(power_input.p_implosion, lasers)
    cas220103.C220103 = scaled_costs["22.1.3. Laser"].total

    return cas220103
