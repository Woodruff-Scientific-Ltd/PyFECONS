from pyfecons.costing.accounting.power_table import PowerTable
from pyfecons.inputs.primary_structure import PrimaryStructure
from pyfecons.units import M_USD, MW, Ratio


def scaled_cost(cost: M_USD, p_et: MW, learning_credit: Ratio) -> M_USD:
    return M_USD(cost * p_et / 1000 * learning_credit)


def compute_engineering_costs(
    primary_structure: PrimaryStructure, power_table: PowerTable
) -> M_USD:
    IN = primary_structure
    p_et = power_table.p_et

    # standard engineering costs
    engineering_costs = M_USD(
        scaled_cost(IN.analyze_costs, p_et, IN.learning_credit)
        + scaled_cost(IN.unit1_seismic_costs, p_et, IN.learning_credit)
        + scaled_cost(IN.reg_rev_costs, p_et, IN.learning_credit)
    )
    # add system PGA costs
    return M_USD(engineering_costs + IN.get_pga_costs().eng_costs)


def compute_fabrication_costs(
    primary_structure: PrimaryStructure, power_table: PowerTable
) -> M_USD:
    IN = primary_structure
    p_et = power_table.p_et

    # standard fabrication costs
    fabrication_costs = M_USD(
        scaled_cost(IN.unit1_fab_costs, p_et, IN.learning_credit)
        + scaled_cost(IN.unit10_fabcosts, p_et, IN.learning_credit)
    )
    # add system PGA costs
    return M_USD(fabrication_costs + IN.get_pga_costs().fab_costs)
