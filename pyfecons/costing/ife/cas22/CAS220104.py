from pyfecons.costing.categories.cas220103_lasers import CAS220103Lasers
from pyfecons.costing.ife.cas22.nif_costs import (
    get_nif_scaled_costs,
    get_nif_replacements,
)
from pyfecons.data import CAS220104IgnitionLasers
from pyfecons.inputs.lasers import Lasers
from pyfecons.inputs.power_input import PowerInput
from pyfecons.report import TemplateProvider


def cas_220104_ignition_laser_costs(
    power_input: PowerInput, lasers: Lasers, cas220103: CAS220103Lasers
) -> TemplateProvider:
    # 22.1.4 Ignition laser
    cas220104 = CAS220104IgnitionLasers()

    scaled_costs = get_nif_scaled_costs(power_input.p_ignition, lasers)
    replacements = get_nif_replacements(scaled_costs)

    replacements["C220103"] = str(round(cas220103.C220103))
    cas220104.C220104 = scaled_costs["22.1.3. Laser"].total
    replacements["C220104XX"] = str(round(cas220104.C220104))
    # TODO missing value for C22010402 in template

    cas220104.template_file = "CAS220104_IFE_DT.tex"
    cas220104.replacements = replacements
    return cas220104
