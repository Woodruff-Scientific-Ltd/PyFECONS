from pyfecons.units import M_USD


def compute_instrumentation_and_control_costs() -> M_USD:
    # Source: page 576, account 12,
    # https://netl.doe.gov/projects/files/CostAndPerformanceBaselineForFossilEnergyPlantsVolume1BituminousCoalAndNaturalGasToElectricity_101422.pdf
    return M_USD(85)
