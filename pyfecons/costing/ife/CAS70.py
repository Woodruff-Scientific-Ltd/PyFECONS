from pyfecons.costing.calculations.conversions import to_m_usd
from pyfecons.units import M_USD
from pyfecons.data import Data, TemplateProvider
from pyfecons.inputs import Inputs


def cas_70(inputs: Inputs, data: Data) -> TemplateProvider:
    # Cost Category  70 Annualized O&M Cost (AOC)
    OUT = data.cas70

    c_om = 60 * data.power_table.p_net * 1000
    # TODO what's this C750000? When do we include it?
    # C750000 = 0.1 * (C220000) scheduled replacement costs

    OUT.C700000 = to_m_usd(c_om) # + C750000

    OUT.template_file = 'CAS700000.tex'
    OUT.tex_path = 'Modified/' + OUT.template_file
    OUT.replacements = {
        'C700000': round(OUT.C700000)
    }
    return OUT