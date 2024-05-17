from pyfecons.costing.ife.cas22.nif_costs import get_nif_scaled_costs, get_nif_replacements
from pyfecons.data import Data, TemplateProvider, CAS220104IgnitionLasers
from pyfecons.inputs import Inputs


def cas_220104_ignition_lasers(inputs: Inputs, data: Data) -> TemplateProvider:
    # 22.1.4 Ignition laser
    OUT: CAS220104IgnitionLasers = data.cas220104
    assert isinstance(OUT, CAS220104IgnitionLasers)

    scaled_costs = get_nif_scaled_costs(inputs.power_table.p_implosion, inputs.lasers)
    replacements = get_nif_replacements(scaled_costs)

    replacements['C220103'] = str(round(data.cas220103.C220103))
    OUT.C220104 = scaled_costs['22.1.3. Laser'].total
    replacements['C220104XX'] = str(round(OUT.C220104))
    # TODO missing value for C22010402 in template

    OUT.template_file = 'CAS220104_IFE_DT.tex'
    OUT.tex_path = 'Modified/' + OUT.template_file
    OUT.replacements = replacements
    return OUT

