from pyfecons.inputs import Inputs
from pyfecons.data import Data
import math

def GenerateData(inputs: Inputs, data:Data, figures:dict):
    
    basic = inputs.basic
    IN = data.power_table
    OUT = data.cas10

    #Cost Category 10: Pre-construction Costs

    #Cost Category 11: Land and Land Rights
    OUT.C110000 = math.sqrt(basic.n_mod) * (IN.p_neutron / (239 * 0.9) + basic.p_nrl/(239 * 0.9))

    #Cost Category 12 – Site Permits

    OUT.C120000 = 10

    #Cost Category 13 – Plant Licensing
    # https://world-nuclear.org/information-library/economic-aspects/economics-of-nuclear-power.aspx

    OUT.C130000 = 200

    #Cost Category 14 – Plant Permits

    OUT.C140000 = 5

    #Cost Category 15 – Plant Studies

    OUT.C150000 = 5

    #Cost Category 16 – Plant Reports

    OUT.C160000 = 2

    #Cost Category 17 – Other Pre-Construction Costs

    OUT.C170000 = 1

    #Cost Cetegory 19 - Contingency

    OUT.C190000 = 0.1 * (OUT.C110000 + OUT.C120000 + OUT.C130000 + OUT.C140000 + OUT.C150000 + OUT.C160000 + OUT.C170000)

    #Cost Category 10

    OUT.C100000 = OUT.C110000 + OUT.C120000 + OUT.C130000 + OUT.C140000 + OUT.C150000 + OUT.C160000 + OUT.C170000