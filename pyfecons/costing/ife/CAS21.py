from pyfecons.units import M_USD
from pyfecons.data import Data
from pyfecons.report import TemplateProvider
from pyfecons.inputs.all_inputs import AllInputs


def cas_21(inputs: AllInputs, data: Data) -> TemplateProvider:
    # Cost Category 21: Buildings
    OUT = data.cas21
    p_et = data.power_table.p_et

    # Buildings come out to be 470$/kW gross, so if we are looking at a gross power of 1GW, we have:
    # TODO - reference for constants

    # 21.01.00,,Site improvements and facs,,20.7,,,,,2019,1.19,
    OUT.C210100 = M_USD(268 / 1e3 * p_et)

    # 21.02.00,,Fusion Heat Island Building,Concrete & Steel,131.6,48.3,48.3,60,140000,2009,1.42,
    OUT.C210200 = M_USD(186.8 / 1e3 * p_et)

    # 21.03.00,,Turbine building,Steel ,45.3,48.3,48.3,30,70000,2019,1.19,
    OUT.C210300 = M_USD(54.0 / 1e3 * p_et)

    # 21.04.00,,Heat exchanger building,Concrete & Steel,31.7,48.3,48.3,15,35000,2019,1.19,
    OUT.C210400 = M_USD(37.8 / 1e3 * p_et)

    # 21.05.00,,Power supply & energy storage,Concrete & Steel,9.1,9.7,9.7,6.0,560,2019,1.19,
    OUT.C210500 = M_USD(10.8 / 1e3 * p_et)

    # 21.06.00,,Reactor auxiliaries,Concrete & Steel,4.5,4.8,4.8,3.0,70,2019,1.19,
    OUT.C210600 = M_USD(5.4 / 1e3 * p_et)

    # 21.07.00,,Hot cell,Concrete & Steel,65.8,24.2,24.2,60,35000,2013,1.42,
    OUT.C210700 = M_USD(93.4 / 1e3 * p_et)

    # 21.08.00,,Reactor services,Steel frame,13.2,4.8,4.8,10,233,2013,1.42,
    OUT.C210800 = M_USD(18.7 / 1e3 * p_et)

    # 21.09.00,,Service water,Steel frame,0.2,1.3,4.0,4.0,21,2019,1.19,
    OUT.C210900 = M_USD(0.3 / 1e3 * p_et)

    # 21.10.00,,Fuel storage,Steel frame,0.9,5.0,15.0,2.5,188,2019,1.19,
    OUT.C211000 = M_USD(1.1 / 1e3 * p_et)

    # 21.11.00,,Control room,Steel frame,0.7,4.0,12.0,2,96,2019,1.19,
    OUT.C211100 = M_USD(0.9 / 1e3 * p_et)

    # 21.12.00,,Onsite AC power,Steel frame,0.7,3.6,10.8,1.8,70,2019,1.19,
    OUT.C211200 = M_USD(0.8 / 1e3 * p_et)

    # 21.13.00,,Administration,Steel frame,3.7,20.0,60.0,10,12000,2019,1.19,
    OUT.C211300 = M_USD(4.4 / 1e3 * p_et)

    # 21.14.00,,Site services,Steel frame,1.3,7.3,22.0,3.7,593,2019,1.19,
    OUT.C211400 = M_USD(1.6 / 1e3 * p_et)

    # 21.15.00,,Cryogenics,Steel frame,2.0,11.0,33.0,5.5,2003,2019,1.19,
    OUT.C211500 = M_USD(2.4 / 1e3 * p_et)

    # 21.16.00,,Security,Steel frame,0.7,4.0,12.0,2,96,2019,1.19,
    OUT.C211600 = M_USD(0.9 / 1e3 * p_et)

    # 21.17.00,,Ventilation stack,Steel cylinder & concrete foundation,22.7,,,120,,2019,1.19,
    OUT.C211700 = M_USD(27.0 / 1e3 * p_et)

    OUT.C210000 = M_USD(
        OUT.C210100
        + OUT.C210200
        + OUT.C210300
        + OUT.C210400
        + OUT.C210500
        + OUT.C210600
        + OUT.C210700
        + OUT.C210800
        + OUT.C210900
        + OUT.C211000
        + OUT.C211100
        + OUT.C211200
        + OUT.C211300
        + OUT.C211400
        + OUT.C211500
        + OUT.C211600
        + OUT.C211700
    )

    if inputs.basic.noak:
        OUT.C211900 = M_USD(0)
    else:
        OUT.C211900 = M_USD(0.1 * OUT.C210000)  # 10% contingency

    OUT.C210000 = M_USD(OUT.C210000 + OUT.C211900)

    OUT.template_file = "CAS210000.tex"
    OUT.replacements = {
        "C210000": round(OUT.C210000, 1),
        "C210100": round(OUT.C210100, 1),
        "C210200": round(OUT.C210200, 1),
        "C210300": round(OUT.C210300, 1),
        "C210400": round(OUT.C210400, 1),
        "C210500": round(OUT.C210500, 1),
        "C210600": round(OUT.C210600, 1),
        "C210700": round(OUT.C210700, 1),
        "C210800": round(OUT.C210800, 1),
        "C210900": round(OUT.C210900, 1),
        "C211000": round(OUT.C211000, 1),
        "C211100": round(OUT.C211100, 1),
        "C211200": round(OUT.C211200, 1),
        "C211300": round(OUT.C211300, 1),
        "C211400": round(OUT.C211400, 1),
        "C211500": round(OUT.C211500, 1),
        "C211600": round(OUT.C211600, 1),
        "C211700": round(OUT.C211700, 1),
        "C211900": round(OUT.C211900, 1),
    }
    return OUT
