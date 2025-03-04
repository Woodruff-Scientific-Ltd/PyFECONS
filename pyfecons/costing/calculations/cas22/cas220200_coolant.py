from pyfecons.data import Data
from pyfecons.inputs.all_inputs import AllInputs
from pyfecons.report import TemplateProvider
from pyfecons.units import Count, MW, M_USD

# TODO - review this section since there is lots of commented code


def cas_2202_main_and_secondary_coolant_costs(
    inputs: AllInputs, data: Data
) -> TemplateProvider:
    # MAIN AND SECONDARY COOLANT Cost Category 22.2
    OUT = data.cas2202
    OUT.C220201 = compute_primary_coolant_costs(
        inputs.basic.n_mod, data.power_table.p_net
    )
    OUT.C220202 = compute_intermediate_coolant_costs(data.power_table.p_th)
    OUT.C220203 = compute_secondary_coolant_costs()
    # Main heat-transfer system (NSSS)
    OUT.C220200 = M_USD(OUT.C220201 + OUT.C220202 + OUT.C220203)

    OUT.template_file = "CAS220200_DT.tex"
    OUT.replacements = {
        "C220200": round(OUT.C220200),
        "C220201": round(OUT.C220201),
        "C220202": round(OUT.C220202),
        "C220203": round(OUT.C220203),  # TODO not in template
        "primaryC": inputs.blanket.primary_coolant.display_name,
        "secondaryC": inputs.blanket.secondary_coolant.display_name,
    }
    return OUT


def compute_primary_coolant_costs(n_mod: Count, p_net: MW) -> M_USD:
    # Li(f), PbLi, He:                %Primary coolant(i):
    # C_22_2_1  = 233.9 * (PTH/3500)^0.55

    # am assuming a linear scaling	%Li(f), PbLi, He:
    # C220201  = 268.5  * (float(basic.n_mod) * power_table.p_th / 3500) * inflation_1992_2024

    # Primary coolant(i):  1.85 is due to inflation%the CPI scaling of 1.71 comes from:
    # https://www.bls.gov/data/inflation_calculator.htm scaled relative to 1992 dollars (despite 2003 publication date)
    # this is the Sheffield cost for a 1GWe system
    return M_USD(166 * (float(n_mod) * p_net / 1000))


def compute_intermediate_coolant_costs(p_th: MW) -> M_USD:
    # OC, H2O(g)
    # C_22_2_1  = 75.0 * (PTH/3500)^0.55
    # Intermediate coolant system
    return M_USD(40.6 * (p_th / 3500) ** 0.55)


def compute_secondary_coolant_costs() -> M_USD:
    # Secondary coolant system
    # 75.0 * (PTH/3500)^0.55
    return M_USD(0)
