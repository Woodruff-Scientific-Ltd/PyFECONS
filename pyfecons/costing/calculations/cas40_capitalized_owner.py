from pyfecons.costing.categories.cas200000 import CAS20
from pyfecons.costing.categories.cas400000 import CAS40
from pyfecons.inputs.lsa_levels import LsaLevels
from pyfecons.units import M_USD


def cas40_capitalized_owner_costs(lsa_levels: LsaLevels, cas20: CAS20) -> CAS40:
    # Cost Category 40 Capitalized Owner’s Cost (COC)
    cas40 = CAS40()

    # TODO determine cost basis, ask simon
    cas40.C400000LSA = M_USD(lsa_levels.fac_91[lsa_levels.lsa - 1] * cas20.C200000)
    # TODO explanation for this section? We ignore all costing after this.
    cas40.C400000 = cas40.C400000LSA

    # Cost Category 41 – Staff Recruitment and Training
    cas40.C410000 = M_USD(0)

    # Cost Category 42 – Staff Housing
    cas40.C420000 = M_USD(0)

    # Cost Category 43 – Staff Salary-Related Costs
    cas40.C430000 = M_USD(0)

    # Cost Category 44 – Other Owner’s Costs
    cas40.C440000 = M_USD(0)

    # TODO why is this here?
    # cas40.C400000 = M_USD(cas40.C410000 + cas40.C420000 + cas40.C430000 + cas40.C440000)

    cas40.template_file = "CAS400000.tex"
    cas40.replacements = {
        "lsaLevel": lsa_levels.lsa,  # TODO - not in template
        "C400000LSA": round(cas40.C400000LSA),
        "C400000XXX": round(cas40.C400000),  # TODO - not in template
    }
    return cas40
