from pyfecons.costing.accounting.power_table import PowerTable
from pyfecons.costing.calculations.conversions import eur_to_usd
from pyfecons.data import CAS220107
from pyfecons.inputs.basic import Basic
from pyfecons.inputs.power_supplies import PowerSupplies
from pyfecons.units import M_USD


def cas_220107_power_supply_costs(
    basic: Basic, power_supplies: PowerSupplies, power_table: PowerTable
) -> CAS220107:
    power_supplies = power_supplies
    cas220107 = CAS220107()

    # Cost Category 22.1.7 Power supplies
    cas220107.C22010701 = M_USD(power_table.p_coils * power_supplies.cost_per_watt)

    # Scaled relative to ITER for a 500MW fusion power system
    # TODO where does 1552.24 and 269.6 come from?
    # kIUA exchange rate in USD
    kIUA = eur_to_usd(1552.24 * 1e-3)
    cas220107.C22010702 = M_USD(
        269.6 * basic.p_nrl / 500 * power_supplies.learning_credit * kIUA
    )
    cas220107.C220107 = M_USD(cas220107.C22010701 + cas220107.C22010702)

    cas220107.template_file = "CAS220107_MFE.tex"
    cas220107.replacements = {
        "C22010700": round(cas220107.C220107),
        "C22010701": round(cas220107.C22010701),
        "C22010702": round(cas220107.C22010702),
        "PNRL": round(basic.p_nrl),
    }
    return cas220107
