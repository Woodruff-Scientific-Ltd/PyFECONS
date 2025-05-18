from pyfecons.enums import FuelType
from pyfecons.costing.accounting.power_table import PowerTable
from pyfecons.inputs.basic import Basic
from pyfecons.inputs.power_input import PowerInput
from pyfecons.units import MW, Ratio


def power_balance(basic: Basic, power_input: PowerInput) -> PowerTable:
    # power balance
    # All power values are in MW
    power_table = PowerTable()
    p_nrl = basic.p_nrl

    if basic.fuel_type == FuelType.PB11 or FuelType.DD:
        power_table.p_alpha = p_nrl
        power_table.p_neutron = MW(0)
    else:
        power_table.p_alpha = p_nrl * 3.52 / 17.58
        power_table.p_neutron = p_nrl - power_table.p_alpha

    power_table.p_aux = MW(power_input.p_trit + power_input.p_house)
    power_table.p_th = MW(
        power_input.mn * power_table.p_neutron
        + power_table.p_alpha
        + power_input.p_input
        + power_input.eta_th
        * (power_input.fpcppf * power_input.eta_p + power_input.f_sub)
        * (power_input.mn * power_table.p_neutron + power_table.p_alpha)
    )
    power_table.p_et = MW(power_input.eta_th * power_table.p_th)
    power_table.p_loss = MW(power_table.p_th - power_table.p_et)
    power_table.gain_e = Ratio(power_table.p_et / power_input.p_input)
    power_table.p_pump = MW(power_input.fpcppf * power_table.p_et)
    power_table.p_sub = MW(power_input.f_sub * power_table.p_et)
    power_table.q_sci = Ratio(p_nrl / power_input.p_input)
    power_table.q_eng = Ratio(
        power_input.eta_th
        * (
            power_input.mn * power_table.p_neutron
            + power_table.p_alpha
            + power_table.p_pump
            + power_input.p_input
        )
        / (
            power_input.p_target
            + power_table.p_pump
            + power_table.p_sub
            + power_table.p_aux
            + power_input.p_cryo
            + power_input.p_implosion / power_input.eta_pin1
            + power_input.p_ignition / power_input.eta_pin2
        )
    )
    power_table.rec_frac = Ratio(1 / power_table.q_eng)
    power_table.p_net = (1 - 1 / power_table.q_eng) * power_table.p_et

    return power_table
