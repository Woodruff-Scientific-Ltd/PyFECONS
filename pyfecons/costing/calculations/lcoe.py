from pyfecons.costing.accounting.power_table import PowerTable
from pyfecons.costing.calculations.conversions import m_to_usd
from pyfecons.costing.categories.cas700000 import CAS70
from pyfecons.costing.categories.cas800000 import CAS80
from pyfecons.costing.categories.cas900000 import CAS90
from pyfecons.costing.categories.lcoe import LCOE
from pyfecons.inputs.basic import Basic
from pyfecons.units import M_USD


def lcoe_costs(
    basic: Basic, power_table: PowerTable, cas70: CAS70, cas80: CAS80, cas90: CAS90
) -> LCOE:
    # LCOE = Localized Cost of Electricity
    lcoe = LCOE()

    # TODO double check the units here. Name the numerator and denominator.
    lcoe.C1000000 = M_USD(
        (
            m_to_usd(cas90.C900000)
            + (m_to_usd(cas70.C700000) + m_to_usd(cas80.C800000))
            * (1 + basic.yearly_inflation) ** basic.plant_lifetime
        )
        / (8760 * power_table.p_net * float(basic.n_mod) * basic.plant_availability)
    )
    lcoe.C2000000 = M_USD(lcoe.C1000000 / 10)

    lcoe.template_file = "LCOE.tex"
    lcoe.replacements = {
        "C1000000": round(lcoe.C1000000, 1),
        "C2000000": round(lcoe.C2000000, 1),
        "C700000": round(cas70.C700000, 1),
        "C800000": round(cas80.C800000, 1),
        "C900000": round(cas90.C900000, 1),
        "PNET": round(power_table.p_net, 3),
        "lifeY": round(basic.plant_lifetime),
        "yinflation": 100 * round(basic.yearly_inflation, 3),
        "PAVAIL": round(basic.plant_availability, 2),
    }
    return lcoe
