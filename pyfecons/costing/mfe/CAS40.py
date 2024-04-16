from pyfecons import M_USD
from pyfecons.inputs import Inputs
from pyfecons.data import Data

CAS_400000_TEX = 'CAS400000.tex'


def GenerateData(inputs: Inputs, data: Data, figures: dict):
    # Cost Category 40 Capitalized Owner’s Cost (COC)
    OUT = data.cas40
    IN = inputs.lsa_levels

    OUT.C400000LSA = M_USD(IN.fac_91[IN.lsa - 1] * data.cas20.C200000)
    # TODO explanation for this section? We ignore all costing after this.
    OUT.C400000 = OUT.C400000LSA

    # Cost Category 41 – Staff Recruitment and Training
    OUT.C410000 = M_USD(0)

    # Cost Category 42 – Staff Housing
    OUT.C420000 = M_USD(0)

    # Cost Category 43 – Staff Salary-Related Costs
    OUT.C430000 = M_USD(0)

    # Cost Category 44 – Other Owner’s Costs
    OUT.C440000 = M_USD(0)

    # OUT.C400000 = M_USD(OUT.C410000 + OUT.C420000 + OUT.C430000 + OUT.C440000)

    OUT.template_file = CAS_400000_TEX
    OUT.replacements = {
        'lsaLevel': IN.lsa,
        'C400000LSA': round(OUT.C400000LSA),
        'C400000000': round(OUT.C400000),  # TODO - not in template
    }
