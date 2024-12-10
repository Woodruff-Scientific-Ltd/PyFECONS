import math
from pyfecons.inputs import Inputs
from pyfecons.data import Data, TemplateProvider
from pyfecons.units import M_USD


def cas_10(inputs: Inputs, data: Data) -> TemplateProvider:
    basic = inputs.basic
    IN = data.power_table
    OUT = data.cas10

    # Cost Category 10: Pre-construction Costs

    # Cost Category 11: Land and Land Rights
    # TODO - what are the magic numbers 239 and 0.9?
    OUT.C110000 = M_USD(
        math.sqrt(basic.n_mod) * (IN.p_neutron / 239 * 0.9 + basic.p_nrl / 239 * 0.9)
    )

    # Cost Category 12 – Site Permits
    OUT.C120000 = M_USD(10)

    # Cost Category 13 – Plant Licensing
    # Source: Midpoint of estimation from 'Capital Costs' section of
    #   https://world-nuclear.org/information-library/economic-aspects/economics-of-nuclear-power.aspx
    OUT.C130000 = M_USD(210)

    # Cost Category 14 – Plant Permits
    OUT.C140000 = M_USD(5)

    # Cost Category 15 – Plant Studies
    OUT.C150000 = M_USD(5)

    # Cost Category 16 – Plant Reports
    OUT.C160000 = M_USD(2)

    # Cost Category 17 – Other Pre-Construction Costs
    OUT.C170000 = M_USD(1)

    # Cost Cetegory 19 - Contingency
    OUT.C190000 = M_USD(
        0
        if basic.noak
        else 0.1
        * (
            OUT.C110000
            + OUT.C120000
            + OUT.C130000
            + OUT.C140000
            + OUT.C150000
            + OUT.C160000
            + OUT.C170000
        )
    )

    # Cost Category 10
    OUT.C100000 = M_USD(
        OUT.C110000
        + OUT.C120000
        + OUT.C130000
        + OUT.C140000
        + OUT.C150000
        + OUT.C160000
        + OUT.C170000
        + OUT.C190000
    )

    OUT.template_file = "CAS100000.tex"
    OUT.replacements = {
        "Nmod": str(basic.n_mod),
        "C100000": str(OUT.C100000),
        "C110000": str(OUT.C110000),
        "C120000": str(OUT.C120000),
        "C130000": str(OUT.C130000),
        "C140000": str(OUT.C140000),
        "C150000": str(OUT.C150000),
        "C160000": str(OUT.C160000),
        "C170000": str(OUT.C170000),
        "C190000": str(OUT.C190000),
    }
    return OUT
