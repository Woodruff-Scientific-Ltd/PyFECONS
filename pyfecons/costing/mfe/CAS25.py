from pyfecons import M_USD
from pyfecons.costing.calculations.conversions import inflation_factor_2019_2024
from pyfecons.inputs import Inputs
from pyfecons.data import Data, TemplateProvider

CAS_250000_TEX = 'CAS250000.tex'


def GenerateData(inputs: Inputs, data: Data) -> list[TemplateProvider]:
    # Cost Category 25 Miscellaneous Plant Equipment
    # No cost basis stated
    OUT = data.cas25

    # From NETL https://netl.doe.gov/projects/files/CostAndPerformanceBaselineForFossilEnergyPlantsVolume1BituminousCoalAndNaturalGasToElectricity_101422.pdf
    OUT.C250000 = M_USD(float(inputs.basic.n_mod) * data.power_table.p_et * 0.038 * inflation_factor_2019_2024)

    OUT.template_file = CAS_250000_TEX
    OUT.tex_path = 'Modified/' + OUT.template_file
    OUT.replacements = {
        'C250000': round(data.cas25.C250000, 1)
    }
    return [OUT]