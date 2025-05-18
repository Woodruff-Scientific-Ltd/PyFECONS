from pyfecons.costing.accounting.power_table import PowerTable
from pyfecons.costing.calculations.conversions import inflation_factor_2019_2024
from pyfecons.costing.categories.cas250000 import CAS25
from pyfecons.inputs.basic import Basic
from pyfecons.units import M_USD


def cas25_misc_plant_equipment_costs(basic: Basic, power_table: PowerTable) -> CAS25:
    # Cost Category 25 Miscellaneous Plant Equipment
    # No cost basis stated
    cas25 = CAS25()

    # From NETL https://netl.doe.gov/projects/files/CostAndPerformanceBaselineForFossilEnergyPlantsVolume1BituminousCoalAndNaturalGasToElectricity_101422.pdf
    cas25.C250000 = M_USD(
        float(basic.n_mod) * power_table.p_et * 0.038 * inflation_factor_2019_2024
    )
    return cas25
