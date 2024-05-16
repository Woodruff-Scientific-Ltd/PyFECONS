from pyfecons.costing.ife.cas22.nif_costs import get_nif_scaled_costs, NifCost
from pyfecons.data import Data, TemplateProvider, CAS220103Lasers
from pyfecons.inputs import Inputs


def cas_220103_lasers(inputs: Inputs, data: Data) -> TemplateProvider:
    # Cost Category 22.1.3: Lasers
    OUT: CAS220103Lasers = data.cas220103
    assert isinstance(OUT, CAS220103Lasers)

    scaled_costs = get_nif_scaled_costs(inputs.power_table.p_implosion, inputs.lasers)
    replacements = get_replacements(scaled_costs)

    OUT.C220103 = scaled_costs['22.1.3. Laser'].total
    replacements['C220103'] = str(round(OUT.C220103))

    OUT.template_file = 'CAS220103_IFE_DT.tex'
    OUT.tex_path = 'Modified/' + OUT.template_file
    OUT.replacements = replacements
    return OUT


def get_replacements(scaled_costs: dict[str, NifCost]) -> dict[str, str]:
    replacements = {}
    for nif_cost in scaled_costs.values():
        replacements[nif_cost.base_key + 'Procurement'] = str(round(nif_cost.procurement, 1))
        replacements[nif_cost.base_key + 'Design'] = str(round(nif_cost.design, 1))
        replacements[nif_cost.base_key + 'Assembly'] = str(round(nif_cost.assembly, 1))
        replacements[nif_cost.base_key + 'Total'] = str(round(nif_cost.total, 1))
    return replacements
