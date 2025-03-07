from pyfecons.costing.calculations.conversions import to_m_usd
from pyfecons.data import CAS80
from pyfecons.inputs.basic import Basic
from pyfecons.inputs.blanket import Blanket
from pyfecons.units import Kilograms


def cas80_annualized_fuel_costs(basic: Basic, blanket: Blanket) -> CAS80:
    # Cost Category 80: Annualized Fuel Cost (AFC)
    cas80 = CAS80()

    # TODO - why are there three calculations of c_f here?
    # c_f = 0.03 * (8760 * PNET*NMOD * p_a) / (1 + yinflation )**lifeY #hours * power = MWh
    # c_f = 50

    # the mass of deuterium https://physics.nist.gov/cgi-bin/cuu/Value?md
    m_D = Kilograms(3.342 * 10 ** (-27))

    # u_D ($/kg) = 2175 ($/kg) from STARFIRE * 1.12345/0.42273 [GDP IPD ratio for 2019/1980]
    u_D = 2175
    c_f = (
        float(basic.n_mod)
        * basic.p_nrl
        * 1e6
        * 3600
        * 8760
        * u_D
        * m_D
        * basic.plant_availability
        / (17.58 * 1.6021e-13)
    )

    cas80.C800000 = to_m_usd(c_f)

    cas80.template_file = "CAS800000_DT.tex"
    cas80.replacements = {
        "C800000": round(cas80.C800000, 2),
        "primaryC": blanket.primary_coolant.display_name,
        "secondaryC": blanket.secondary_coolant.display_name,
    }
    return cas80
