from pyfecons.data import Data, TemplateProvider
from pyfecons.units import M_USD


def cas_2207_instrumentation_and_control(data: Data) -> TemplateProvider:
    # Cost Category 22.7 Instrumentation and Control
    OUT = data.cas2207
    # Source: page 576, account 12,
    # https://netl.doe.gov/projects/files/CostAndPerformanceBaselineForFossilEnergyPlantsVolume1BituminousCoalAndNaturalGasToElectricity_101422.pdf
    OUT.C220700 = M_USD(85)

    OUT.template_file = 'CAS220700.tex'
    OUT.tex_path = 'Modified/' + OUT.template_file
    OUT.replacements = {
        'C220700': str(data.cas2207.C220700)
    }
    return OUT
