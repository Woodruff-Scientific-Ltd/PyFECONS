from pyfecons.costing.calculations.conversions import m_to_usd
from pyfecons.units import M_USD
from pyfecons.data import Data
from pyfecons.report import TemplateProvider
from pyfecons.inputs.all_inputs import AllInputs


def lcoe(inputs: AllInputs, data: Data) -> TemplateProvider:
    # LCOE = Localized Cost of Electricity
    OUT = data.lcoe
    basic = inputs.basic

    # TODO double check the units here
    OUT.C1000000 = M_USD(
        (
            m_to_usd(data.cas90.C900000)
            + (m_to_usd(data.cas70.C700000) + m_to_usd(data.cas80.C800000))
            * (1 + basic.yearly_inflation) ** basic.plant_lifetime
        )
        / (
            8760
            * data.power_table.p_net
            * float(basic.n_mod)
            * basic.plant_availability
        )
    )
    OUT.C2000000 = M_USD(OUT.C1000000 / 10)

    OUT.template_file = "LCOE.tex"
    OUT.replacements = {
        "C1000000": round(OUT.C1000000, 1),
        "C2000000": round(OUT.C2000000, 1),
        "C700000": round(data.cas70.C700000, 1),
        "C800000": round(data.cas80.C800000, 1),
        "C900000": round(data.cas90.C900000, 1),
        "PNET": round(data.power_table.p_net, 3),
        "lifeY": round(basic.plant_lifetime),
        "yinflation": 100 * round(basic.yearly_inflation, 3),
        "PAVAIL": round(basic.plant_availability, 2),
    }
    return OUT
