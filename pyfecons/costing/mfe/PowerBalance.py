from pyfecons.enums import FuelType
from pyfecons.costing.accounting.power_table import PowerTable
from pyfecons.inputs.basic import Basic
from pyfecons.inputs.power_input import PowerInput
from pyfecons.units import MW, Unknown


def power_balance(basic: Basic, power_input: PowerInput) -> PowerTable:
    power_table = PowerTable()
    power_table.p_alpha = compute_p_alpha(basic.p_nrl, basic.fuel_type)
    power_table.p_neutron = MW(basic.p_nrl - power_table.p_alpha)
    power_table.p_cool = MW(power_input.p_tfcool + power_input.p_pfcool)
    power_table.p_aux = MW(power_input.p_trit + power_input.p_house)
    power_table.p_coils = MW(power_input.p_tf + power_input.p_pf)
    power_table.p_th = MW(
        power_input.mn * power_table.p_neutron
        + power_input.p_input
        + power_input.eta_th
        * (power_input.fpcppf * power_input.eta_p + power_input.f_sub)
        * (power_input.mn * power_table.p_neutron)
    )
    power_table.p_the = MW(power_input.eta_th * power_table.p_th)
    power_table.p_dee = MW(power_input.eta_de * power_table.p_alpha)
    power_table.p_et = MW(power_table.p_dee + power_table.p_the)
    power_table.p_loss = MW(power_table.p_th - power_table.p_the - power_table.p_dee)
    power_table.p_pump = MW(power_input.fpcppf * power_table.p_the)
    power_table.p_sub = MW(power_input.f_sub * power_table.p_the)
    power_table.q_sci = Unknown(basic.p_nrl / power_input.p_input)
    power_table.q_eng = Unknown(
        (
            power_input.eta_th
            * (
                power_input.mn * power_table.p_neutron
                + power_table.p_pump
                + power_input.p_input
            )
            + power_input.eta_de * power_table.p_alpha
        )
        / (
            power_table.p_coils
            + power_table.p_pump
            + power_table.p_sub
            + power_table.p_aux
            + power_table.p_cool
            + power_input.p_cryo
            + power_input.p_input / power_input.eta_pin
        )
    )
    power_table.rec_frac = 1 / power_table.q_eng
    power_table.p_net = MW((1 - 1 / power_table.q_eng) * power_table.p_et)

    return power_table


def compute_p_alpha(p_nrl: MW, fuel_type: FuelType) -> MW:
    # Charged particle power in fuel_type reaction - from ratio of total energy for fuel_type
    #   https://en.wikipedia.org/wiki/Nuclear_fusion
    if fuel_type == FuelType.DT:
        return MW(p_nrl * 3.52 / 17.58)
    elif fuel_type == FuelType.DD:
        return MW(p_nrl * (0.5 * 3.02 / (3.02 + 1.01) + 0.5 * 0.82 / (0.82 + 2.45)))
    elif fuel_type == FuelType.DHE3:
        return MW(p_nrl * 14.7 / (14.7 + 3.6))
    elif fuel_type == FuelType.PB11:
        return MW(p_nrl * 8.7 / 8.7)
