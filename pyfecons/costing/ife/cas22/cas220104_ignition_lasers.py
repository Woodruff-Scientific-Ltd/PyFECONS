from pyfecons.costing.categories.cas220104_ignition_lasers import (
    CAS220104IgnitionLasers,
)
from pyfecons.costing.ife.cas22.nif_costs import get_nif_scaled_costs
from pyfecons.inputs.lasers import Lasers
from pyfecons.inputs.power_input import PowerInput


def cas_220104_ignition_laser_costs(
    power_input: PowerInput, lasers: Lasers
) -> CAS220104IgnitionLasers:
    # 22.1.4 Ignition laser
    cas220104 = CAS220104IgnitionLasers()
    cas220104.scaled_costs = get_nif_scaled_costs(power_input.p_ignition, lasers)
    cas220104.C220104 = cas220104.scaled_costs["22.1.3. Laser"].total
    return cas220104
