from pyfecons.costing.calculations.conversions import to_m_usd
from pyfecons.costing.categories.cas220101 import CAS220101
from pyfecons.data import CAS220111
from pyfecons.inputs.basic import Basic
from pyfecons.inputs.installation import Installation
from pyfecons.units import USD, Years, Count, Meters, M_USD


def cas_220111_installation_costs(
    basic: Basic, installation: Installation, cas220101: CAS220101
) -> CAS220111:
    # Cost Category 22.1.11 Installation costs
    cas220111 = CAS220111()

    cas220111.C220111 = compute_installation_costs(
        installation.labor_rate, basic.construction_time, basic.n_mod, cas220101.axis_ir
    )
    cas220111.template_file = "CAS220111.tex"
    cas220111.replacements = {
        "C220111": str(cas220111.C220111),
        "constructionTime": round(basic.construction_time),
        "billingRate": round(installation.labor_rate),
    }
    return cas220111


def compute_installation_costs(
    labor_rate: USD, construction_time: Years, n_mod: Count, axis_ir: Meters
) -> M_USD:
    # Calculations
    labor_rate_m_usd = to_m_usd(labor_rate)
    # TODO what are 20 and 4? Should they be inputs?
    construction_worker = 20 * axis_ir / 4
    costs = {
        # TODO what are 20 and 300? Should they be inputs?
        "C_22_1_11_in": float(n_mod)
        * construction_time
        * (labor_rate_m_usd * 20 * 300),
        # TODO for all constants, should they be inputs?
        # TODO why + 0 for all of these
        "C_22_1_11_1_in": float(n_mod)
        * ((labor_rate_m_usd * 200 * construction_worker) + 0),
        # 22.1 first wall blanket
        "C_22_1_11_2_in": float(n_mod)
        * ((labor_rate_m_usd * 150 * construction_worker) + 0),  # 22.2 shield
        "C_22_1_11_3_in": float(n_mod)
        * ((labor_rate_m_usd * 100 * construction_worker) + 0),  # coils
        "C_22_1_11_4_in": float(n_mod)
        * ((labor_rate_m_usd * 30 * construction_worker) + 0),
        # supplementary heating
        "C_22_1_11_5_in": float(n_mod)
        * ((labor_rate_m_usd * 60 * construction_worker) + 0),  # primary structure
        "C_22_1_11_6_in": float(n_mod)
        * ((labor_rate_m_usd * 200 * construction_worker) + 0),  # vacuum system
        "C_22_1_11_7_in": float(n_mod)
        * ((labor_rate_m_usd * 400 * construction_worker) + 0),  # power supplies
        "C_22_1_11_8_in": 0,  # guns or divertor
        "C_22_1_11_9_in": float(n_mod)
        * ((labor_rate_m_usd * 200 * construction_worker) + 0),
        # direct energy converter
        "C_22_1_11_10_in": 0,  # ECRH
    }
    # Total cost calculations
    return M_USD(sum(costs.values()))
