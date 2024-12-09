from pyfecons.costing.calculations.conversions import inflation_factor_2019_2024
from pyfecons.inputs import Inputs
from pyfecons.data import Data, TemplateProvider
from pyfecons.units import M_USD


def cas_23(inputs: Inputs, data: Data) -> TemplateProvider:
    # Cost Category 23 Turbine Plant Equipment
    OUT = data.cas23

    # Source: page 507 https://netl.doe.gov/projects/files/CostAndPerformanceBaselineForFossilEnergyPlantsVolume1BituminousCoalAndNaturalGasToElectricity_101422.pdf
    OUT.C230000 = M_USD(
        float(inputs.basic.n_mod)
        * data.power_table.p_et
        * 0.219
        * inflation_factor_2019_2024
    )

    OUT.template_file = "CAS230000.tex"
    OUT.replacements = {"C230000": round(data.cas23.C230000, 1)}
    return OUT
