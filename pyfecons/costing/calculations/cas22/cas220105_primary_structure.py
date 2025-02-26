from pyfecons.costing.accounting.power_table import PowerTable
from pyfecons.data import Data
from pyfecons.inputs.all_inputs import AllInputs
from pyfecons.inputs.primary_structure import PrimaryStructure
from pyfecons.report import TemplateProvider
from pyfecons.units import M_USD, MW, Ratio


def cas_220105_primary_structure_costs(
    inputs: AllInputs, data: Data
) -> TemplateProvider:
    # 22.1.5 primary structure
    OUT = data.cas220105

    OUT.C22010501 = compute_engineering_costs(
        inputs.primary_structure, data.power_table
    )
    OUT.C22010502 = compute_fabrication_costs(
        inputs.primary_structure, data.power_table
    )

    # total cost calculation
    OUT.C220105 = M_USD(OUT.C22010501 + OUT.C22010502)
    OUT.template_file = "CAS220105.tex"
    OUT.replacements = {
        "C22010501": str(round(OUT.C22010501)),
        "C22010502": str(round(OUT.C22010502)),
        "C22010500": str(round(OUT.C220105)),
        "systPGA": str(round(inputs.primary_structure.syst_pga.value, 1)),
        "PNRL": str(round(inputs.basic.p_nrl)),
    }
    return OUT


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
