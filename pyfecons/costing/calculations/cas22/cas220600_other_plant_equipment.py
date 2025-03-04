from pyfecons.costing.accounting.power_table import PowerTable
from pyfecons.data import CAS2206
from pyfecons.units import MW, M_USD


def cas_2206_other_reactor_plant_equipment_costs(power_table: PowerTable) -> CAS2206:
    # Cost Category 22.6 Other Reactor Plant Equipment
    cas2206 = CAS2206()
    cas2206.C220600 = compute_other_plant_equipment_costs(power_table.p_net)
    cas2206.template_file = "CAS220600.tex"
    cas2206.replacements = {"C220600": round(cas2206.C220600)}
    return cas2206


def compute_other_plant_equipment_costs(p_net: MW) -> M_USD:
    # from Waganer, L., 2013. ARIES Cost Account Documentation. [pdf] San Diego: University of California, San Diego.
    #   Available at: https://cer.ucsd.edu/_files/publications/UCSD-CER-13-01.pdf
    return M_USD(11.5 * (p_net / 1000) ** 0.8)
