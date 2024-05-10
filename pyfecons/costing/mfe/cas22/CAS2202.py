from pyfecons.data import Data, TemplateProvider
from pyfecons.inputs import Inputs
from pyfecons.units import M_USD


def cas_2202_main_and_secondary_coolant(inputs: Inputs, data: Data) -> TemplateProvider:
    # TODO - review this section since there is lots of commented code

    # MAIN AND SECONDARY COOLANT Cost Category 22.2
    OUT = data.cas2202

    # Li(f), PbLi, He:                %Primary coolant(i):
    # C_22_2_1  = 233.9 * (PTH/3500)^0.55

    # am assuming a linear scaling	%Li(f), PbLi, He:
    # C220201  = 268.5  * (float(basic.n_mod) * power_table.p_th / 3500) * inflation_1992_2024

    # Primary coolant(i):  1.85 is due to inflation%the CPI scaling of 1.71 comes from:
    # https://www.bls.gov/data/inflation_calculator.htm scaled relative to 1992 dollars (despite 2003 publication date)
    # this is the Sheffield cost for a 1GWe system
    OUT.C220201 = M_USD(166 * (float(inputs.basic.n_mod) * data.power_table.p_net / 1000))

    # OC, H2O(g)
    # C_22_2_1  = 75.0 * (PTH/3500)^0.55
    # Intermediate coolant system
    OUT.C220202 = M_USD(40.6 * (data.power_table.p_th / 3500) ** 0.55)

    OUT.C220203 = M_USD(0)
    # Secondary coolant system
    # 75.0 * (PTH/3500)^0.55

    # Main heat-transfer system (NSSS)
    OUT.C220200 = M_USD(OUT.C220201 + OUT.C220202 + OUT.C220203)
    OUT.template_file = 'CAS220200_DT.tex'
    OUT.tex_path = 'Modified/' + OUT.template_file
    OUT.replacements = {
        'C220200': OUT.C220200,
        'C220201': OUT.C220201,
        'C220202': OUT.C220202,
        'C220203': OUT.C220203,  # TODO not in template
        'primaryC': inputs.blanket.primary_coolant.display_name,
        'secondaryC': inputs.blanket.secondary_coolant.display_name,
    }
    return OUT
