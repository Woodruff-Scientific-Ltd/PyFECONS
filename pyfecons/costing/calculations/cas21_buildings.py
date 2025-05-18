from pyfecons.costing.accounting.power_table import PowerTable
from pyfecons.costing.calculations.conversions import k_to_m_usd
from pyfecons.enums import FuelType, ReactorType
from pyfecons.costing.categories.cas210000 import CAS21
from pyfecons.inputs.basic import Basic
from pyfecons.units import M_USD


def cas_21_building_costs(basic: Basic, power_table: PowerTable) -> CAS21:
    # Cost Category 21: Buildings
    cas21 = CAS21()
    p_et = power_table.p_et

    # Buildings come out to be 470$/kW gross, so if we are looking at a gross power of 1GW, we have:

    # [1]From NETL reference case B12A
    # [2] Waganer, L.M., 2013. ARIES cost account documentation. San Diego: University of California.

    # 0.5 from lack of Tritium - we don't need so much structure in the containment building.
    fuel_scaling_factor = get_fuel_scaling_factor(basic.reactor_type, basic.fuel_type)

    # 21.01.00,,Site improvements and facs. Source: [1] cost account 13, page 134
    cas21.C210100 = M_USD(k_to_m_usd(268) * p_et * fuel_scaling_factor)

    # 21.02.00,,Fusion Heat Island Building,Concrete & Steel,. Source: [2], pg 11.
    cas21.C210200 = M_USD(k_to_m_usd(186.8) * p_et * fuel_scaling_factor)

    # 21.03.00,,Turbine building,Steel. Source: [1] cost account 14.2, page 134
    cas21.C210300 = M_USD(k_to_m_usd(54.0) * p_et)

    # 21.04.00,,Heat exchanger building,Concrete & Steel,Source: [1] cost account 14.2, page 134
    cas21.C210400 = M_USD(k_to_m_usd(37.8) * p_et)

    # 21.05.00,,Power supply & energy storage,Concrete & Steel,Source: scaled from [1] cost account 14.2, page 134
    cas21.C210500 = M_USD(k_to_m_usd(10.8) * p_et)

    # 21.06.00,,Reactor auxiliaries,Concrete & Steel, Source: [1] cost account 14.8, page 134
    cas21.C210600 = M_USD(k_to_m_usd(5.4) * p_et)

    # 21.07.00,,Hot cell,Concrete & Steel, Source: [1] cost account 14.1, page 134
    cas21.C210700 = M_USD(k_to_m_usd(93.4) * p_et * fuel_scaling_factor)

    # 21.08.00,,Reactor services,Steel frame, Source: scaled from [1] cost account 14.1, page 134
    cas21.C210800 = M_USD(k_to_m_usd(18.7) * p_et)

    # 21.09.00,,Service water,Steel frame, Source: [1] cost account 14.4, page 134
    cas21.C210900 = M_USD(k_to_m_usd(0.3) * p_et)

    # 21.10.00,,Fuel storage,Steel frame, Source: scaled from [1] cost account 14.1, page 134
    cas21.C211000 = M_USD(k_to_m_usd(1.1) * p_et)

    # 21.11.00,,Control room,Steel frame,0.7,4.0,12.0,2,96,2019,1.19,
    cas21.C211100 = M_USD(k_to_m_usd(0.9) * p_et)

    # 21.12.00,,Onsite AC power,Steel frame,0.7,3.6,10.8,1.8,70,2019,1.19,
    cas21.C211200 = M_USD(k_to_m_usd(0.8) * p_et)

    # 21.13.00,,Administration,Steel frame,Source: [1] cost account 14.3, page 134
    cas21.C211300 = M_USD(k_to_m_usd(4.4) * p_et)

    # 21.14.00,,Site services,Steel frame,Source: scaled from [1] cost account 14.6, page 134
    cas21.C211400 = M_USD(k_to_m_usd(1.6) * p_et)

    # 21.15.00,,Cryogenics,Steel frame,Source: scaled from [1] cost account 14.4, page 134
    cas21.C211500 = M_USD(k_to_m_usd(2.4) * p_et)

    # 21.16.00,,Security,Steel frame,Source: scaled from [1] cost account 14.8, page 134
    cas21.C211600 = M_USD(k_to_m_usd(0.9) * p_et)

    # 21.17.00,,Ventilation stack,Steel cylinder & concrete foundation,Source: scaled from [1] cost account 14.3,
    # page 134
    cas21.C211700 = M_USD(k_to_m_usd(27.0) * p_et)

    cas21.C210000 = M_USD(
        cas21.C210100
        + cas21.C210200
        + cas21.C210300
        + cas21.C210400
        + cas21.C210500
        + cas21.C210600
        + cas21.C210700
        + cas21.C210800
        + cas21.C210900
        + cas21.C211000
        + cas21.C211100
        + cas21.C211200
        + cas21.C211300
        + cas21.C211400
        + cas21.C211500
        + cas21.C211600
        + cas21.C211700
    )

    if basic.noak:
        cas21.C211900 = M_USD(0)
    else:
        cas21.C211900 = M_USD(0.1 * cas21.C210000)  # 10% contingency

    cas21.C210000 = M_USD(cas21.C210000 + cas21.C211900)

    return cas21


def get_fuel_scaling_factor(reactor_type: ReactorType, fuel_type: FuelType):
    if reactor_type != ReactorType.MFE:
        return 1.0
    if fuel_type == FuelType.DT:
        return 1.0
    return 0.5
