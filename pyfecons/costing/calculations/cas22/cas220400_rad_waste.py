from pyfecons.costing.calculations.conversions import inflation_1992_2024
from pyfecons.units import MW, M_USD


def compute_radioactive_waste_cost(p_th: MW) -> M_USD:
    # Radioactive waste treatment
    # base cost of 1.96M from Alexeeva, V., Molloy, B., Beestermoeller, R., Black, G., Bradish, D., Cameron, R.,
    #   Keppler, J.H., Rothwell, G., Urso, M.E., Colakoglu, I. and Emeric, J., 2018. Measuring Employment Generated
    #   by the Nuclear Power Sector (No. NEA--7204). Organisation for Economic Co-Operation and Development.
    return M_USD(1.96 * 1e-3 * p_th * inflation_1992_2024)
