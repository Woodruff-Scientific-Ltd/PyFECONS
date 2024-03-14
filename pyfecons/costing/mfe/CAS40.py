from pyfecons import M_USD
from pyfecons.inputs import Inputs
from pyfecons.data import Data


def GenerateData(inputs: Inputs, data: Data, figures: dict):
    OUT = data.cas40

    # Cost Category 40 Capitalized Owner’s Cost (COC)

    OUT.C400000LSA = M_USD(inputs.lsa_levels.fac_91[inputs.lsa_levels.lsa - 1] * data.cas20.C200000)
    OUT.C400000 = OUT.C400000LSA

    # Cost Category 41 – Staff Recruitment and Training

    # C410000=0

    # Cost Category 42 – Staff Housing

    # C420000=0

    # Cost Category 43 – Staff Salary-Related Costs

    # C430000 = 0

    # Cost Category 44 – Other Owner’s Costs

    # C440000 = 0

    # C400000 = C410000 + C420000 + C430000 + C440000
