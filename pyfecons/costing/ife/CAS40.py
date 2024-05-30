from pyfecons.units import M_USD
from pyfecons.data import Data, TemplateProvider
from pyfecons.inputs import Inputs


def cas_40(inputs: Inputs, data: Data) -> TemplateProvider:
    IN = inputs.lsa_levels
    OUT = data.cas40

    # Cost Category 40 Capitalized Owner’s Cost (COC)
    OUT.C400000LSA = M_USD(IN.fac_91[IN.lsa - 1] * data.cas20.C200000)
    OUT.C400000 = OUT.C400000LSA

    # Cost Category 41 – Staff Recruitment and Training
    OUT.C410000 = M_USD(0)

    # Cost Category 42 – Staff Housing
    OUT.C420000 = M_USD(0)

    # Cost Category 43 – Staff Salary-Related Costs
    OUT.C430000 = M_USD(0)

    # Cost Category 44 – Other Owner’s Costs
    OUT.C440000 = M_USD(0)

    # TODO why is this here?
    # C400000 = C410000 + C420000 + C430000 + C440000

    OUT.template_file = 'CAS400000.tex'
    OUT.replacements = {
        'C400000LSA': round(OUT.C400000LSA),
        'C400000XXX': round(OUT.C400000),  # TODO not in template
    }
    return OUT