from pyfecons.data import Data, TemplateProvider
from pyfecons.inputs import Inputs


def calculate_npv(inputs: Inputs, data: Data) -> TemplateProvider:
    OUT = data.npv

    npv = 0
    CDD = 0  # TODO: figure out what CDD is
    for n in range(int(inputs.basic.plant_lifetime)):
        npv += (
            data.cas90.C900000
            + data.cas220119.C220119
            + data.cas70.C700000
            + data.cas80.C800000
            - (data.cas10.C100000 + CDD)
            * inputs.basic.plant_availability
            * data.power_table.p_net
            * 8760
        ) / (1 + inputs.npv.discount_rate) ** n

    OUT.npv = npv
    OUT.template_file = "NPV.tex"
    OUT.replacements = {
        "NPVval": round(OUT.npv, 2),
        "DiscountRate": round(
            inputs.npv.discount_rate * 100, 2
        ),  # Multiplied by 100 for percentage
    }

    return OUT
