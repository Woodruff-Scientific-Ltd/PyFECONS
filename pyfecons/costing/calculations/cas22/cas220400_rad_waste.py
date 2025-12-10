from pyfecons.costing.accounting.power_table import PowerTable
from pyfecons.costing.calculations.conversions import inflation_1992_2024, k_to_m_usd
from pyfecons.costing.categories.cas220400 import CAS2204
from pyfecons.units import M_USD, MW


def cas_2204_radwaste_costs(power_table: PowerTable) -> CAS2204:
    # Cost Category 22.4 Radwaste
    cas2204 = CAS2204()
    cas2204.C220400 = compute_radioactive_waste_cost(power_table.p_th)
    return cas2204


def compute_radioactive_waste_cost(p_th: MW) -> M_USD:
    # Radioactive waste treatment
    # base cost of 1.96M from Alexeeva, V., Molloy, B., Beestermoeller, R., Black, G., Bradish, D., Cameron, R.,
    #   Keppler, J.H., Rothwell, G., Urso, M.E., Colakoglu, I. and Emeric, J., 2018. Measuring Employment Generated
    #   by the Nuclear Power Sector (No. NEA--7204). Organisation for Economic Co-Operation and Development.
    return k_to_m_usd(1.96 * p_th * inflation_1992_2024)
