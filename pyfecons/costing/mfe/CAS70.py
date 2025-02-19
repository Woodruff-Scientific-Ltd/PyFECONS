from pyfecons.costing.calculations.conversions import to_m_usd
from pyfecons.inputs.all_inputs import AllInputs
from pyfecons.data import Data, TemplateProvider


def cas_70(inputs: AllInputs, data: Data) -> TemplateProvider:
    # Cost Category  70 Annualized O\&M Cost (AOC)
    OUT = data.cas70

    c_om = 60 * data.power_table.p_net * 1000

    # TODO what's up with the commented code here?
    # C750000 = 0.1 * (C220000) scheduled replacement costs

    OUT.C700000 = to_m_usd(c_om)  # + C750000

    OUT.template_file = "CAS700000.tex"
    OUT.replacements = {"C700000": round(data.cas70.C700000)}
    return OUT
