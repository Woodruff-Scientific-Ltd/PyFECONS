import numpy as np

from pyfecons import M_USD
from pyfecons.data import Data, TemplateProvider
from pyfecons.inputs import Inputs


def GenerateData(inputs: Inputs, data: Data) -> list[TemplateProvider]:
    # Cost Category 10: Pre-construction Costs
    OUT = data.cas10
    IN = inputs.basic

    # Cost Category 11: Land and Land Rights
    # TODO where does 239 & 0.9 come from?
    OUT.C110000 = M_USD(np.sqrt(IN.n_mod) * (data.power_table.p_neutron / 239 * 0.9 + IN.p_nrl / 239 * 0.9))

    # Cost Category 12 – Site Permits
    OUT.C120000 = M_USD(10)

    # Cost Category 13 – Plant Licensing
    # https://world-nuclear.org/information-library/economic-aspects/economics-of-nuclear-power.aspx
    OUT.C130000 = M_USD(200)

    # Cost Category 14 – Plant Permits
    OUT.C140000 = M_USD(5)

    # Cost Category 15 – Plant Studies
    OUT.C150000 = M_USD(5)

    # Cost Category 16 – Plant Reports
    OUT.C160000 = M_USD(2)

    # Cost Category 17 – Other Pre-Construction Costs
    OUT.C170000 = M_USD(1)

    # Cost Cetegory 19 - Contingency
    if IN.noak:
        OUT.C190000 = M_USD(0)
    else:
        OUT.C190000 = M_USD(0.1 * (OUT.C110000 + OUT.C120000 + OUT.C130000 + OUT.C140000
                                   + OUT.C150000 + OUT.C160000 + OUT.C170000))

    # Cost Category 10
    OUT.C100000 = M_USD(OUT.C110000 + OUT.C120000 + OUT.C130000 + OUT.C140000 + OUT.C150000 + OUT.C160000 + OUT.C170000)

    OUT.template_file = 'CAS100000.tex'
    OUT.tex_path = 'Modified/' + OUT.template_file
    OUT.replacements = {
        'Nmod': IN.n_mod,
        'C100000': round(OUT.C100000),
        'C110000': round(OUT.C110000),
        'C120000': round(OUT.C120000),
        'C130000': round(OUT.C130000),
        'C140000': round(OUT.C140000),
        'C150000': round(OUT.C150000),
        'C160000': round(OUT.C160000),
        'C170000': round(OUT.C170000),
        'C190000': round(OUT.C190000),
    }
    return [OUT]