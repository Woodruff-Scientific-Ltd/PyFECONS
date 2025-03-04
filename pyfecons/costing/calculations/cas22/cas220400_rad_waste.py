from pyfecons.costing.accounting.power_table import PowerTable
from pyfecons.costing.calculations.conversions import inflation_1992_2024, k_to_m_usd
from pyfecons.data import Data, CAS2204
from pyfecons.report import TemplateProvider
from pyfecons.units import MW, M_USD


def cas_2204_radwaste_costs(power_table: PowerTable) -> CAS2204:
    # Cost Category 22.4 Radwaste
    cas2204 = CAS2204()
    cas2204.C220400 = compute_radioactive_waste_cost(power_table.p_th)
    cas2204.template_file = "CAS220400.tex"
    cas2204.replacements = {"C220400": round(cas2204.C220400, 1)}
    return cas2204


def compute_radioactive_waste_cost(p_th: MW) -> M_USD:
    # Radioactive waste treatment
    # base cost of 1.96M from Alexeeva, V., Molloy, B., Beestermoeller, R., Black, G., Bradish, D., Cameron, R.,
    #   Keppler, J.H., Rothwell, G., Urso, M.E., Colakoglu, I. and Emeric, J., 2018. Measuring Employment Generated
    #   by the Nuclear Power Sector (No. NEA--7204). Organisation for Economic Co-Operation and Development.
    return k_to_m_usd(1.96 * p_th * inflation_1992_2024)
