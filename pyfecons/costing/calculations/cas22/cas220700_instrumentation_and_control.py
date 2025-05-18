from pyfecons.costing.categories.cas220700 import CAS2207
from pyfecons.units import M_USD


def cas_2207_instrumentation_and_control_costs() -> CAS2207:
    # Cost Category 22.7 Instrumentation and Control
    cas2207 = CAS2207()
    cas2207.C220700 = compute_instrumentation_and_control_costs()
    return cas2207


def compute_instrumentation_and_control_costs() -> M_USD:
    # Source: page 576, account 12,
    # https://netl.doe.gov/projects/files/CostAndPerformanceBaselineForFossilEnergyPlantsVolume1BituminousCoalAndNaturalGasToElectricity_101422.pdf
    return M_USD(85)
