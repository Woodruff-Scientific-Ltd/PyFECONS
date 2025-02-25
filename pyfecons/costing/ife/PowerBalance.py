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
        * (power_input.mn * power_table.p_neutron + power_table.p_alpha + power_table.p_pump + power_input.p_input)
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

    power_table.template_file = "powerTableIFEDT.tex"
    # TODO round everything by 1
    power_table.replacements = {
        "PNRL": round(p_nrl, 1),
        "PALPHA": round(power_table.p_alpha, 1),
        "PNEUTRON": round(power_table.p_neutron, 1),
        "MN": round(power_input.mn, 1),
        "FPCPPF": round(power_input.fpcppf, 1),
        "FSUB": round(power_input.f_sub, 1),
        "PTRIT": round(power_input.p_trit, 1),
        "PHOUSE": round(power_input.p_house, 1),
        "PAUX": round(power_table.p_aux, 1),
        "PCRYO": round(power_input.p_cryo, 1),
        "ETAPIN1": round(power_input.eta_pin1, 1),
        "ETAPIN2": round(power_input.eta_pin2, 1),
        "ETAP": round(power_input.eta_p, 1),
        "ETATH": round(power_input.eta_th, 1),
        "PIMPLOSION": round(power_input.p_implosion, 1),
        "PIGNITION": round(power_input.p_ignition, 1),
        "PTH": round(power_table.p_th, 1),
        "PET": round(power_table.p_et, 1),
        "PLOSS": round(power_table.p_loss, 1),
        "GAINE": round(power_table.gain_e, 1),
        "PTARGET": round(power_input.p_target, 1),
        "PMACHINERY": round(power_input.p_machinery, 1),
        "PSUB": round(power_table.p_sub, 1),
        "QS": round(power_table.q_sci, 1),
        "QE": round(power_table.q_eng, 1),
        "EPSILON": round(power_table.rec_frac, 1),
        "PNET": round(power_table.p_net, 1),
        "PP": round(power_table.p_pump, 1),
        "PIN": round(power_input.p_input, 1),
    }
    return power_table
