from pyfecons.data import Data
from pyfecons.report import TemplateProvider
from pyfecons.units import M_USD


def cas_2207_instrumentation_and_control_costs(data: Data) -> TemplateProvider:
    # Cost Category 22.7 Instrumentation and Control
    OUT = data.cas2207
    OUT.C220700 = compute_instrumentation_and_control_costs()
    OUT.template_file = "CAS220700.tex"
    OUT.replacements = {"C220700": round(data.cas2207.C220700)}
    return OUT


def compute_instrumentation_and_control_costs() -> M_USD:
    # Source: page 576, account 12,
    # https://netl.doe.gov/projects/files/CostAndPerformanceBaselineForFossilEnergyPlantsVolume1BituminousCoalAndNaturalGasToElectricity_101422.pdf
    return M_USD(85)
