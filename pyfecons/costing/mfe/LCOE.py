from pyfecons.inputs import Inputs
from pyfecons.data import Data, TemplateProvider
from pyfecons.units import M_USD


def lcoe(inputs: Inputs, data: Data) -> TemplateProvider:
    # LCOE = _____ Cost of Electricity
    OUT = data.lcoe

    OUT.C1000000 = M_USD(
        (data.cas90.C900000 * 1e6 + (data.cas70.C700000 * 1e6 + data.cas80.C800000 * 1e6)
         * (1 + inputs.basic.yearly_inflation) ** inputs.basic.plant_lifetime)
        / (8760 * data.power_table.p_net * (float(inputs.basic.n_mod) * inputs.basic.plant_availability)))
    OUT.C2000000 = M_USD(OUT.C1000000 / 10)

    OUT.template_file = 'LCOE.tex'
    OUT.replacements = {
        'C1000000': round(OUT.C1000000, 1),
        'C2000000': round(OUT.C2000000, 1),
        'C700000': round(data.cas70.C700000, 1),
        'C800000': round(data.cas80.C800000, 1),
        'C900000': round(data.cas90.C900000, 1),
        'PNET': round(data.power_table.p_net, 3),
        'lifeY': round(inputs.basic.plant_lifetime),
        'yinflation': 100 * round(inputs.basic.yearly_inflation, 3),
        'PAVAIL': round(inputs.basic.plant_availability, 2),
    }
    return OUT
