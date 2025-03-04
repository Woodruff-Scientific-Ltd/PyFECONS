from pyfecons.costing.accounting.power_table import PowerTable
from pyfecons.costing.calculations.conversions import inflation_factor_2019_2024
from pyfecons.data import CAS23
from pyfecons.inputs.basic import Basic
from pyfecons.units import M_USD


def cas23_turbine_plant_equipment_costs(basic: Basic, power_table: PowerTable) -> CAS23:
    # Cost Category 23 Turbine Plant Equipment
    cas23 = CAS23()

    # Source: page 507 https://netl.doe.gov/projects/files/CostAndPerformanceBaselineForFossilEnergyPlantsVolume1BituminousCoalAndNaturalGasToElectricity_101422.pdf
    cas23.C230000 = M_USD(
        float(basic.n_mod) * power_table.p_et * 0.219 * inflation_factor_2019_2024
    )

    cas23.template_file = "CAS230000.tex"
    cas23.replacements = {"C230000": round(cas23.C230000, 1)}
    return cas23
