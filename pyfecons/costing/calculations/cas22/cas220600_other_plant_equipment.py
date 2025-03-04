from pyfecons.data import Data
from pyfecons.report import TemplateProvider
from pyfecons.units import MW, M_USD


def cas_2206_other_reactor_plant_equipment_costs(data: Data) -> TemplateProvider:
    # Cost Category 22.6 Other Reactor Plant Equipment
    OUT = data.cas2206
    OUT.C220600 = compute_other_plant_equipment_costs(data.power_table.p_net)
    OUT.template_file = "CAS220600.tex"
    OUT.replacements = {"C220600": round(OUT.C220600)}
    return OUT


def compute_other_plant_equipment_costs(p_net: MW) -> M_USD:
    # from Waganer, L., 2013. ARIES Cost Account Documentation. [pdf] San Diego: University of California, San Diego.
    #   Available at: https://cer.ucsd.edu/_files/publications/UCSD-CER-13-01.pdf
    return M_USD(11.5 * (p_net / 1000) ** 0.8)
