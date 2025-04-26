from pyfecons.costing.categories.cas220107 import CAS220107
from pyfecons.inputs.all_inputs import PowerSupplies
from pyfecons.inputs.basic import Basic
from pyfecons.units import M_USD


def cas_220107_power_supply_costs(
    basic: Basic, power_supplies: PowerSupplies
) -> CAS220107:
    # Cost Category 22.1.7 Power supplies
    cas220107 = CAS220107()

    # Power supplies for confinement
    cas220107.C22010701 = M_USD(
        power_supplies.p_compress
        * basic.implosion_frequency
        * power_supplies.cost_per_watt
    )

    # Scaled relative to ITER for a 500MW fusion power system
    # assuming 1kIUA equals $2 M #cost in kIUA
    cas220107.C22010702 = M_USD(
        269.6 * basic.p_nrl / 500 * power_supplies.learning_credit * 2
    )
    cas220107.C220107 = M_USD(cas220107.C22010701 + cas220107.C22010702)

    # TODO - is this ever a value?
    # scaled relative to the Woodruff Scientific PF bank designed for FLARE: 200kV, 400kA, 0.5MJ
    # C22010702 = 30
    # C220107 = 30
    return cas220107
