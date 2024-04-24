from pyfecons import M_USD
from pyfecons.inputs import Inputs
from pyfecons.data import Data, TemplateProvider

CAS_210000_TEX = 'CAS210000.tex'


def GenerateData(inputs: Inputs, data: Data, figures: dict) -> list[TemplateProvider]:
    IN = data.power_table
    OUT = data.cas21

    # Cost Category 21: Buildings

    # Buildings come out to be 470$/kW gross, so if we are looking at a gross power of 1GW, we have:

    # [1]From NETL reference case B12A
    # [2] Waganer, L.M., 2013. ARIES cost account documentation. San Diego: University of California.

    # 21.01.00,,Site improvements and facs. Source: [1] cost account 13, page 134
    # 0.5 comes from use of DD
    OUT.C210100 = M_USD(268 / 1e3 * IN.p_et * 0.5)

    # 21.02.00,,Fusion Heat Island Building,Concrete & Steel,. Source: [2], pg 11.
    # 0.5 comes from use of DD - we don't need so much structure in the containment building.
    OUT.C210200 = M_USD(186.8 / 1e3 * IN.p_et * 0.5)

    # 21.03.00,,Turbine building,Steel. Source: [1] cost account 14.2, page 134
    OUT.C210300 = M_USD(54.0 / 1e3 * IN.p_et)

    # 21.04.00,,Heat exchanger building,Concrete & Steel,Source: [1] cost account 14.2, page 134
    OUT.C210400 = M_USD(37.8 / 1e3 * IN.p_et)

    # 21.05.00,,Power supply & energy storage,Concrete & Steel,Source: scaled from [1] cost account 14.2, page 134
    OUT.C210500 = M_USD(10.8 / 1e3 * IN.p_et)

    # 21.06.00,,Reactor auxiliaries,Concrete & Steel, Source: [1] cost account 14.8, page 134
    OUT.C210600 = M_USD(5.4 / 1e3 * IN.p_et)

    # 21.07.00,,Hot cell,Concrete & Steel, Source: [1] cost account 14.1, page 134
    # 0.5 from use of DD
    OUT.C210700 = M_USD(93.4 / 1e3 * IN.p_et * 0.5)

    # 21.08.00,,Reactor services,Steel frame, Source: scaled from [1] cost account 14.1, page 134
    OUT.C210800 = M_USD(18.7 / 1e3 * IN.p_et)

    # 21.09.00,,Service water,Steel frame, Source: [1] cost account 14.4, page 134
    OUT.C210900 = M_USD(0.3 / 1e3 * IN.p_et)

    # 21.10.00,,Fuel storage,Steel frame, Source: scaled from [1] cost account 14.1, page 134
    OUT.C211000 = M_USD(1.1 / 1e3 * IN.p_et)

    # 21.11.00,,Control room,Steel frame,0.7,4.0,12.0,2,96,2019,1.19,
    OUT.C211100 = M_USD(0.9 / 1e3 * IN.p_et)

    # 21.12.00,,Onsite AC power,Steel frame,0.7,3.6,10.8,1.8,70,2019,1.19,
    OUT.C211200 = M_USD(0.8 / 1e3 * IN.p_et)

    # 21.13.00,,Administration,Steel frame,Source: [1] cost account 14.3, page 134
    OUT.C211300 = M_USD(4.4 / 1e3 * IN.p_et)

    # 21.14.00,,Site services,Steel frame,Source: scaled from [1] cost account 14.6, page 134
    OUT.C211400 = M_USD(1.6 / 1e3 * IN.p_et)

    # 21.15.00,,Cryogenics,Steel frame,Source: scaled from [1] cost account 14.4, page 134
    OUT.C211500 = M_USD(2.4 / 1e3 * IN.p_et)

    # 21.16.00,,Security,Steel frame,Source: scaled from [1] cost account 14.8, page 134
    OUT.C211600 = M_USD(0.9 / 1e3 * IN.p_et)

    # 21.17.00,,Ventilation stack,Steel cylinder & concrete foundation,Source: scaled from [1] cost account 14.3,
    # page 134
    OUT.C211700 = M_USD(27.0 / 1e3 * IN.p_et)

    OUT.C210000 = M_USD(OUT.C210100 + OUT.C210200 + OUT.C210300 + OUT.C210400 + OUT.C210500 + OUT.C210600
                        + OUT.C210700 + OUT.C210800 + OUT.C210900 + OUT.C211000 + OUT.C211100 + OUT.C211200
                        + OUT.C211300 + OUT.C211400 + OUT.C211500 + OUT.C211600 + OUT.C211700)

    OUT.C211900 = M_USD(0 if inputs.basic.noak else 0.1 * OUT.C210000)  # 10% contingency

    OUT.C210000 = M_USD(OUT.C210000 + OUT.C211900)

    OUT.template_file = CAS_210000_TEX
    OUT.tex_path = 'Modified/' + OUT.template_file
    OUT.replacements = {
        'C210000': str(round(data.cas21.C210000, 1)),
        'C210100': str(round(data.cas21.C210100, 1)),
        'C210200': str(round(data.cas21.C210200, 1)),
        'C210300': str(round(data.cas21.C210300, 1)),
        'C210400': str(round(data.cas21.C210400, 1)),
        'C210500': str(round(data.cas21.C210500, 1)),
        'C210600': str(round(data.cas21.C210600, 1)),
        'C210700': str(round(data.cas21.C210700, 1)),
        'C210800': str(round(data.cas21.C210800, 1)),
        'C210900': str(round(data.cas21.C210900, 1)),
        'C211000': str(round(data.cas21.C211000, 1)),
        'C211100': str(round(data.cas21.C211100, 1)),
        'C211200': str(round(data.cas21.C211200, 1)),
        'C211300': str(round(data.cas21.C211300, 1)),
        'C211400': str(round(data.cas21.C211400, 1)),
        'C211500': str(round(data.cas21.C211500, 1)),
        'C211600': str(round(data.cas21.C211600, 1)),
        'C211700': str(round(data.cas21.C211700, 1)),
        'C211900': str(round(data.cas21.C211900, 1)),  # TODO - not in the template file
    }
    return [OUT]
