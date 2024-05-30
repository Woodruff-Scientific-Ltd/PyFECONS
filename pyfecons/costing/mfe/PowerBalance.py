from pyfecons.enums import FuelType
from pyfecons.inputs import Inputs
from pyfecons.data import Data, TemplateProvider
from pyfecons.units import MW, Unknown


def power_balance(inputs: Inputs, data: Data) -> TemplateProvider:
    basic = inputs.basic
    IN = inputs.power_table
    OUT = data.power_table
    OUT.p_alpha = compute_p_alpha(basic.p_nrl, basic.fuel_type)
    OUT.p_neutron = MW(basic.p_nrl - OUT.p_alpha)
    OUT.p_cool = MW(IN.p_tfcool + IN.p_pfcool)
    OUT.p_aux = MW(IN.p_trit + IN.p_house)
    OUT.p_coils = MW(IN.p_tf + IN.p_pf)
    OUT.p_th = MW(IN.mn * OUT.p_neutron + IN.p_input + IN.eta_th
                  * (IN.fpcppf * IN.eta_p + IN.f_sub) * (IN.mn * OUT.p_neutron))
    OUT.p_the = MW(IN.eta_th * OUT.p_th)
    OUT.p_dee = MW(IN.eta_de * OUT.p_alpha)
    OUT.p_et = MW(OUT.p_dee + OUT.p_the)
    OUT.p_loss = MW(OUT.p_th - OUT.p_the - OUT.p_dee)
    OUT.p_pump = MW(IN.fpcppf * OUT.p_the)
    OUT.p_sub = MW(IN.f_sub * OUT.p_the)
    OUT.q_sci = Unknown(basic.p_nrl / IN.p_input)
    OUT.q_eng = Unknown((IN.eta_th * (IN.mn * OUT.p_neutron + OUT.p_pump + IN.p_input) + IN.eta_de * OUT.p_alpha)
                        / (OUT.p_coils + OUT.p_pump + OUT.p_sub + OUT.p_aux + OUT.p_cool + IN.p_cryo
                           + IN.p_input / IN.eta_pin))
    OUT.rec_frac = 1 / OUT.q_eng
    OUT.p_net = MW((1 - 1 / OUT.q_eng) * OUT.p_et)

    OUT.template_file = 'powerTableMFEDT.tex'
    OUT.replacements = {
        # Ordered by occurrence in template
        # 1. Output power
        'PNRL': inputs.basic.p_nrl,  # Fusion Power
        'PALPHA': OUT.p_alpha,  # Alpha Power
        'PNEUTRON': OUT.p_neutron,  # Neutron Power
        'MN___': inputs.power_table.mn,  # Neutron Energy Multiplier
        'ETAP__': inputs.power_table.eta_p,  # Pumping power capture efficiency
        'PTH___': OUT.p_th,  # Thermal Power
        'ETATH': inputs.power_table.eta_th,  # Thermal conversion efficiency
        'PET___': OUT.p_et,  # Total (Gross) Electric Power
        # 2. Recirculating power
        'PLOSS': OUT.p_loss,  # Lost Power
        'PCOILS': OUT.p_coils,  # Power into coils
        'PTF___': inputs.power_table.p_tf,  # Power into TF coils
        'PPF___': inputs.power_table.p_pf,  # Power into PF (equilibrium) coils
        'FPCPPF': inputs.power_table.fpcppf,  # Primary Coolant Pumping Power Fraction
        'PPUMP': OUT.p_pump,  # Primary Coolant Pumping Power
        'FSUB': inputs.power_table.f_sub,  # Subsystem and Control Fraction
        'PSUB': OUT.p_sub,  # Subsystem and Control Power
        'PAUX': OUT.p_aux,  # Auxiliary systems
        'PTRIT': inputs.power_table.p_trit,  # Tritium Systems
        'PHOUSE': inputs.power_table.p_house,  # Housekeeping power
        'PCOOL': OUT.p_cool,  # Cooling systems
        'PTFCOOL': inputs.power_table.p_tfcool,  # TF coil cooling
        'PPFCOOL': inputs.power_table.p_pfcool,  # PF coil cooling
        'PCRYO': inputs.power_table.p_cryo,  # Cryo vacuum pumping
        'ETAPIN': inputs.power_table.eta_pin,  # Input power wall plug efficiency
        'PINPUT': inputs.power_table.p_input,  # Input power
        # 3. Outputs
        'QSCI': OUT.q_sci,  # Scientific Q
        'QENG': OUT.q_eng,  # Engineering Q
        'RECFRAC': round(OUT.rec_frac, 3),  # Recirculating power fraction
        'PNET': OUT.p_net,  # Output Power (Net Electric Power)
        # TODO these will be included depending on EnergyConversion type
        # 'ETADE': ETADE,
        # 'PDEE': PDEE,
    }
    return OUT


def compute_p_alpha(p_nrl: MW, fuel_type: FuelType) -> MW:
    # Charged particle power in fuel_type reaction - from ratio of total energy for fuel_type
    #   https://en.wikipedia.org/wiki/Nuclear_fusion
    if fuel_type == FuelType.DT:
        return MW(p_nrl * 3.52 / 17.58)
    elif fuel_type == FuelType.DD:
        return MW(p_nrl * (0.5 * 3.02 / (3.02 + 1.01) + 0.5 * 0.82 / (0.82 + 2.45)))
    elif fuel_type == FuelType.DHE3:
        return MW(p_nrl * 14.7 / (14.7+3.6))
    elif fuel_type == FuelType.PB11:
        return MW(p_nrl * 8.7/8.7)