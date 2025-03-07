from pyfecons.costing.calculations.conversions import to_m_usd
from pyfecons.inputs.all_inputs import AllInputs
from pyfecons.data import Data
from pyfecons.report import TemplateProvider


def cas70_annualized_om_costs(inputs: AllInputs, data: Data) -> TemplateProvider:
    # Cost Category  70 Annualized O&M Cost (AOC)
    OUT = data.cas70

    c_om = 60 * data.power_table.p_net * 1000

    # TODO what's this C750000? When do we include it?
    # C750000 = 0.1 * (C220000) scheduled replacement costs

    OUT.C700000 = to_m_usd(c_om)  # + C750000

    OUT.template_file = "CAS700000.tex"
    OUT.replacements = {"C700000": round(data.cas70.C700000)}
    return OUT
