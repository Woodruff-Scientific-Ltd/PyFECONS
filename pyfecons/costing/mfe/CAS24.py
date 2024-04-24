from pyfecons import M_USD
from pyfecons.inputs import Inputs
from pyfecons.data import Data, TemplateProvider

CAS_240000_TEX = 'CAS240000.tex'


def GenerateData(inputs: Inputs, data: Data, figures: dict) -> list[TemplateProvider]:
    # Cost Category 24 Electric Plant Equipment
    OUT = data.cas24

    # Talk to Simon, see page 508 https://netl.doe.gov/projects/files/CostAndPerformanceBaselineForFossilEnergyPlantsVolume1BituminousCoalAndNaturalGasToElectricity_101422.pdf
    # TODO what do 0.054 & 1.15 represent?
    OUT.C240000 = M_USD(float(inputs.basic.n_mod) * data.power_table.p_et * 0.054 * 1.15)

    OUT.template_file = CAS_240000_TEX
    OUT.tex_path = 'Modified/' + OUT.template_file
    OUT.replacements = {
        'C240000': round(OUT.C240000, 1)
    }
    return [OUT]