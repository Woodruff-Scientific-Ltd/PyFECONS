from pyfecons.data import Data, TemplateProvider
from pyfecons.inputs import Inputs
from pyfecons.units import M_USD


def cas_220105_primary_structure(inputs: Inputs, data: Data) -> TemplateProvider:
    # 22.1.5 primary structure
    IN = inputs.primary_structure
    OUT = data.cas220105

    # lambda function to compute scaled costs in these calculations
    scaled_cost = lambda cost: cost * data.power_table.p_et / 1000 * IN.learning_credit

    # standard engineering costs
    OUT.C22010501 = M_USD(scaled_cost(IN.analyze_costs)
                          + scaled_cost(IN.unit1_seismic_costs)
                          + scaled_cost(IN.reg_rev_costs))

    # standard fabrication costs
    OUT.C22010502 = M_USD(scaled_cost(IN.unit1_fab_costs) + scaled_cost(IN.unit10_fabcosts))

    # add system PGA costs
    pga_costs = IN.get_pga_costs()
    OUT.C22010501 = M_USD(OUT.C22010501 + pga_costs.eng_costs)
    OUT.C22010502 = M_USD(OUT.C22010502 + pga_costs.fab_costs)

    # total cost calculation
    OUT.C220105 = M_USD(OUT.C22010501 + OUT.C22010502)
    OUT.template_file = 'CAS220105.tex'
    OUT.tex_path = 'Modified/' + OUT.template_file
    OUT.replacements = {
        'C22010501': str(OUT.C22010501),
        'C22010502': str(OUT.C22010502),
        'C22010500': str(OUT.C220105),
        'systPGA': str(IN.syst_pga.value),
        'PNRL': str(inputs.basic.p_nrl)
    }
    return OUT
