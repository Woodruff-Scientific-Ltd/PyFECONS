from pyfecons.costing.calculations.conversions import to_m_usd
from pyfecons.units import USD, Years, Count, Meters, M_USD


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
