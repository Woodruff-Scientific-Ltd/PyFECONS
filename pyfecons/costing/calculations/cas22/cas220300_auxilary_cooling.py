from pyfecons.costing.calculations.conversions import inflation_1992_2024
from pyfecons.data import Data
from pyfecons.inputs.all_inputs import AllInputs
from pyfecons.report import TemplateProvider
from pyfecons.units import Count, MW, M_USD


def cas_2203_auxilary_cooling_costs(inputs: AllInputs, data: Data) -> TemplateProvider:
    # Cost Category 22.3  Auxiliary cooling
    OUT = data.cas2203
    OUT.C220300 = compute_auxilary_coolant_costs(
        inputs.basic.n_mod, data.power_table.p_th
    )
    OUT.template_file = "CAS220300.tex"
    OUT.replacements = {"C220300": str(round(OUT.C220300, 1))}
    return OUT


def compute_auxilary_coolant_costs(n_mod: Count, p_th: MW) -> M_USD:
    # Auxiliary cooling systems
    return M_USD(1.10 * 1e-3 * float(n_mod) * p_th * inflation_1992_2024)
