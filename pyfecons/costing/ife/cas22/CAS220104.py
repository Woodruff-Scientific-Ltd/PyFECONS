from pyfecons.costing.ife.cas22.nif_costs import (
    get_nif_scaled_costs,
    get_nif_replacements,
)
from pyfecons.data import Data, CAS220104IgnitionLasers
from pyfecons.report import TemplateProvider
from pyfecons.inputs.all_inputs import AllInputs


def cas_220104_ignition_lasers(inputs: AllInputs, data: Data) -> TemplateProvider:
    # 22.1.4 Ignition laser
    OUT: CAS220104IgnitionLasers = data.cas220104
    assert isinstance(OUT, CAS220104IgnitionLasers)

    scaled_costs = get_nif_scaled_costs(inputs.power_table.p_ignition, inputs.lasers)
    replacements = get_nif_replacements(scaled_costs)

    replacements["C220103"] = str(round(data.cas220103.C220103))
    OUT.C220104 = scaled_costs["22.1.3. Laser"].total
    replacements["C220104XX"] = str(round(OUT.C220104))
    # TODO missing value for C22010402 in template

    OUT.template_file = "CAS220104_IFE_DT.tex"
    OUT.replacements = replacements
    return OUT
