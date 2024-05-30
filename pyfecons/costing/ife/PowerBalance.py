from pyfecons.enums import FuelType
from pyfecons.inputs import Inputs
from pyfecons.data import Data, TemplateProvider
from pyfecons.units import MW, Ratio


def power_balance(inputs: Inputs, data: Data) -> TemplateProvider:
    # power balance
    # All power values are in MW
    OUT = data.power_table
    IN = inputs.power_table
    p_nrl = inputs.basic.p_nrl

    if inputs.basic.fuel_type == FuelType.PB11 or FuelType.DD:
        OUT.p_alpha = p_nrl
        OUT.p_neutron = MW(0)
    else:
        OUT.p_alpha = p_nrl * 3.52 / 17.58
        OUT.p_neutron = p_nrl - OUT.p_alpha

    OUT.p_aux = MW(IN.p_trit + IN.p_house)
    OUT.p_th = MW(IN.mn * OUT.p_neutron + OUT.p_alpha + IN.p_input + IN.eta_th * (IN.fpcppf * IN.eta_p + IN.f_sub)
                  * (IN.mn * OUT.p_neutron + OUT.p_alpha))
    OUT.p_et = MW(IN.eta_th * OUT.p_th)
    OUT.p_loss = MW(OUT.p_th - OUT.p_et)
    OUT.gain_e = Ratio(OUT.p_et / IN.p_input)
    OUT.p_pump = MW(IN.fpcppf * OUT.p_et)
    OUT.p_sub = MW(IN.f_sub * OUT.p_et)
    OUT.q_sci = Ratio(p_nrl / IN.p_input)
    OUT.q_eng = Ratio(IN.eta_th * (IN.mn * OUT.p_neutron + OUT.p_alpha + OUT.p_pump + IN.p_input)
                      / (IN.p_target + OUT.p_pump + OUT.p_sub + OUT.p_aux + IN.p_cryo
                         + IN.p_implosion / IN.eta_pin1 + IN.p_ignition / IN.eta_pin2))
    OUT.rec_frac = Ratio(1 / OUT.q_eng)
    OUT.p_net = (1 - 1 / OUT.q_eng) * OUT.p_et

    OUT.template_file = 'powerTableIFEDT.tex'
    # TODO round everything by 1
    OUT.replacements = {
        'PNRL': round(p_nrl, 1),
        'PALPHA': round(OUT.p_alpha, 1),
        'PNEUTRON': round(OUT.p_neutron, 1),
        'MN': round(IN.mn, 1),
        'FPCPPF': round(IN.fpcppf, 1),
        'FSUB': round(IN.f_sub, 1),
        'PTRIT': round(IN.p_trit, 1),
        'PHOUSE': round(IN.p_house, 1),
        'PAUX': round(OUT.p_aux, 1),
        'PCRYO': round(IN.p_cryo, 1),
        'ETAPIN1': round(IN.eta_pin1, 1),
        'ETAPIN2': round(IN.eta_pin2, 1),
        'ETAP': round(IN.eta_p, 1),
        'ETATH': round(IN.eta_th, 1),
        'PIMPLOSION': round(IN.p_implosion, 1),
        'PIGNITION': round(IN.p_ignition, 1),
        'PTH': round(OUT.p_th, 1),
        'PET': round(OUT.p_et, 1),
        'PLOSS': round(OUT.p_loss, 1),
        'GAINE': round(OUT.gain_e, 1),
        'PTARGET': round(IN.p_target, 1),
        'PMACHINERY': round(IN.p_machinery, 1),
        'PSUB': round(OUT.p_sub, 1),
        'QS': round(OUT.q_sci, 1),
        'QE': round(OUT.q_eng, 1),
        'EPSILON': round(OUT.rec_frac, 1),
        'PNET': round(OUT.p_net, 1),
        'PP': round(OUT.p_pump, 1),
        'PIN': round(IN.p_input, 1),
    }
    return OUT