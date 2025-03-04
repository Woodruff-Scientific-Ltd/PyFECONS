from pyfecons.costing.calculations.conversions import inflation_factor_2019_2024
from pyfecons.inputs.all_inputs import AllInputs
from pyfecons.data import Data
from pyfecons.report import TemplateProvider
from pyfecons.units import M_USD


def cas24_electric_plant_equipment_costs(
    inputs: AllInputs, data: Data
) -> TemplateProvider:
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
