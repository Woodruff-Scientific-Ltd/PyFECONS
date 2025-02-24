from pyfecons.costing.calculations.conversions import inflation_factor_2019_2024
from pyfecons.inputs import Inputs
from pyfecons.data import Data, TemplateProvider
from pyfecons.units import M_USD


def cas_24(inputs: Inputs, data: Data) -> TemplateProvider:
    # Cost Category 24 Electric Plant Equipment
    OUT = data.cas24

    # Source: page 508 https://netl.doe.gov/projects/files/CostAndPerformanceBaselineForFossilEnergyPlantsVolume1BituminousCoalAndNaturalGasToElectricity_101422.pdf
    OUT.C240000 = M_USD(
        float(inputs.basic.n_mod)
        * data.power_table.p_et
        * 0.054
        * inflation_factor_2019_2024
    )

    OUT.template_file = "CAS240000.tex"
    OUT.replacements = {"C240000": round(OUT.C240000, 1)}
    return OUT
