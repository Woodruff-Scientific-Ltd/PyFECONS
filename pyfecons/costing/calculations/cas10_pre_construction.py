import math

from pyfecons.costing.accounting.power_table import PowerTable
from pyfecons.costing.categories.cas100000 import CAS10
from pyfecons.costing.safety.licensing import licensing_safety_addon
from pyfecons.inputs.basic import Basic
from pyfecons.units import M_USD


def cas_10_pre_construction_costs(basic: Basic, power_table: PowerTable) -> CAS10:
    # Cost Category 10: Pre-construction Costs
    cas10 = CAS10()

    # Cost Category 11: Land and Land Rights
    # TODO - what are the magic numbers 239 and 0.9?
    cas10.C110000 = M_USD(
        math.sqrt(basic.n_mod)
        * (power_table.p_neutron / 239 * 0.9 + basic.p_nrl / 239 * 0.9)
    )

    # Cost Category 12 – Site Permits
    cas10.C120000 = M_USD(10)

    # Cost Category 13 – Plant Licensing
    # Base cost from 'Capital Costs' section of
    # https://world-nuclear.org/information-library/economic-aspects/economics-of-nuclear-power.aspx
    base_licensing_cost = M_USD(210)
    # Safety and hazard mitigation addon (region-dependent, applied when enabled)
    cas10.C130000 = base_licensing_cost + licensing_safety_addon(basic)

    # Cost Category 14 – Plant Permits
    cas10.C140000 = M_USD(5)

    # Cost Category 15 – Plant Studies
    cas10.C150000 = M_USD(5)

    # Cost Category 16 – Plant Reports
    cas10.C160000 = M_USD(2)

    # Cost Category 17 – Other Pre-Construction Costs
    cas10.C170000 = M_USD(1)

    # Cost Category 19 - Contingency
    if basic.noak:
        cas10.C190000 = M_USD(0)
    else:
        cas10.C190000 = M_USD(
            0.1
            * (
                cas10.C110000
                + cas10.C120000
                + cas10.C130000
                + cas10.C140000
                + cas10.C150000
                + cas10.C160000
                + cas10.C170000
            )
        )

    # Cost Category 10
    cas10.C100000 = M_USD(
        cas10.C110000
        + cas10.C120000
        + cas10.C130000
        + cas10.C140000
        + cas10.C150000
        + cas10.C160000
        + cas10.C170000
        + cas10.C190000
    )

    return cas10
