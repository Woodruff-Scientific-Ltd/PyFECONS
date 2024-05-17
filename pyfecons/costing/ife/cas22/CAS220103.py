from pyfecons.costing.ife.cas22.nif_costs import get_nif_scaled_costs, get_nif_replacements
from pyfecons.data import Data, TemplateProvider, CAS220103Lasers
from pyfecons.inputs import Inputs


def cas_220103_lasers(inputs: Inputs, data: Data) -> TemplateProvider:
    # Cost Category 22.1.3: Lasers
    OUT: CAS220103Lasers = data.cas220103
    assert isinstance(OUT, CAS220103Lasers)

    scaled_costs = get_nif_scaled_costs(inputs.power_table.p_implosion, inputs.lasers)
    replacements = get_nif_replacements(scaled_costs)

    OUT.C220103 = scaled_costs['22.1.3. Laser'].total
    replacements['C220103'] = str(round(OUT.C220103))

    OUT.template_file = 'CAS220103_IFE_DT.tex'
    OUT.tex_path = 'Modified/' + OUT.template_file
    OUT.replacements = replacements
    return OUT


