from pyfecons.data import Data
from pyfecons.costing.accounting.npv import NPV
from pyfecons.inputs.basic import Basic
from pyfecons.inputs.npv_Input import NpvInput


def calculate_npv(basic: Basic, npv_input: NpvInput, data: Data) -> NPV:
    npv = NPV()

    power_table = data.power_table
    cas10 = data.cas10
    cas220119 = data.cas220119
    cas70 = data.cas70
    cas80 = data.cas80
    cas90 = data.cas90

    npv_val = 0
    CDD = 0  # TODO: figure out what CDD is
    for n in range(int(basic.plant_lifetime)):
        npv_val += (
            cas90.C900000
            + cas220119.C220119
            + cas70.C700000
            + cas80.C800000
            - (cas10.C100000 + CDD)
            * basic.plant_availability
            * power_table.p_net
            * 8760
        ) / (1 + npv_input.discount_rate) ** n

    npv.npv = npv_val
    npv.template_file = "NPV.tex"
    npv.replacements = {
        "NPVval": round(npv.npv, 2),
        "DiscountRate": round(
            npv_input.discount_rate * 100, 2
        ),  # Multiplied by 100 for percentage
    }

    return npv
