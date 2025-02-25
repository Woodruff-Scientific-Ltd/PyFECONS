import math
from pyfecons.costing.categories.cas10 import CAS10
from pyfecons.inputs.basic import Basic
from pyfecons.units import M_USD
from pyfecons.costing.accounting.power_table import PowerTable


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
    # Source: Midpoint of estimation from 'Capital Costs' section of
    # https://world-nuclear.org/information-library/economic-aspects/economics-of-nuclear-power.aspx
    cas10.C130000 = M_USD(210)

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

    cas10.template_file = "CAS100000.tex"
    cas10.replacements = {
        "Nmod": str(basic.n_mod),
        "C100000": str(cas10.C100000),
        "C110000": str(cas10.C110000),
        "C120000": str(cas10.C120000),
        "C130000": str(cas10.C130000),
        "C140000": str(cas10.C140000),
        "C150000": str(cas10.C150000),
        "C160000": str(cas10.C160000),
        "C170000": str(cas10.C170000),
        "C190000": str(cas10.C190000),
    }
    return cas10
