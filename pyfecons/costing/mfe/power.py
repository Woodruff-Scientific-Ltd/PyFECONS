from pyfecons.inputs import Inputs
from pyfecons.data import Data
def GenerateData(inputs: Inputs, data:Data, figures:dict):
    
    basic = inputs.basic
    IN = inputs.power_table
    OUT = data.power_table
    OUT.p_alpha = basic.p_nrl * 3.52 / 17.58
    OUT.p_neutron = basic.p_nrl - OUT.p_alpha
    OUT.p_cool = IN.p_tfcool + IN.p_pfcool
    OUT.p_aux = IN.p_trit + IN.p_house
    OUT.p_coils = IN.p_tf + IN.p_pf
    OUT.p_th = IN.mn + OUT.p_neutron + IN.eta_th \
         * (IN.fpcppf * IN.eta_p + IN.f_sub) \
         * (IN.mn * OUT.p_neutron)
    OUT.p_the = IN.eta_th * OUT.p_th
    OUT.p_dee = IN.eta_de * OUT.p_alpha
    OUT.p_et = OUT.p_dee + OUT.p_the
    OUT.p_loss = OUT.p_th - OUT.p_the - OUT.p_dee
    OUT.p_pump = IN.fpcppf * OUT.p_the
    OUT.p_sub = IN.f_sub * OUT.p_the
    OUT.qsci = basic.p_nrl / IN.p_input
    OUT.qeng = (IN.eta_th * (IN.mn * OUT.p_neutron + OUT.p_pump + IN.p_input)+IN.eta_de*OUT.p_alpha) \
          / (OUT.p_coils + OUT.p_pump + OUT.p_sub + OUT.p_aux + OUT.p_cool + IN.p_cryo + IN.p_input / IN.eta_pin)
    OUT.refrac = 1/OUT.qeng
    OUT.p_net = (1 - 1 / OUT.qeng) * OUT.p_et