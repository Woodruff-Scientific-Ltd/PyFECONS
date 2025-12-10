from pyfecons.costing.accounting.power_table import PowerTable
from pyfecons.costing.calculations.conversions import inflation_factor_2019_2024
from pyfecons.costing.categories.cas240000 import CAS24
from pyfecons.inputs.basic import Basic
from pyfecons.units import M_USD


def cas24_electric_plant_equipment_costs(
    basic: Basic, power_table: PowerTable
) -> CAS24:
    # Cost Category 24 Electric Plant Equipment
    cas24 = CAS24()

    # Source: page 508 https://netl.doe.gov/projects/files/CostAndPerformanceBaselineForFossilEnergyPlantsVolume1BituminousCoalAndNaturalGasToElectricity_101422.pdf
    cas24.C240000 = M_USD(
        float(basic.n_mod) * power_table.p_et * 0.054 * inflation_factor_2019_2024
    )
    return cas24
