from pyfecons.costing.calculations.conversions import to_m_usd
from pyfecons.inputs import Inputs
from pyfecons.data import Data, TemplateProvider
from pyfecons.units import Kilograms


def cas_80(inputs: Inputs, data: Data) -> TemplateProvider:
    # Cost Category 80: Annualized Fuel Cost (AFC)
    OUT = data.cas80

    # TODO - why are there three calculations of c_f here?
    # c_f = 0.03 * (8760 * PNET*NMOD * p_a) / (1 + yinflation )**lifeY #hours * power = MWh
    # c_f = 50

    # the mass of deuterium https://physics.nist.gov/cgi-bin/cuu/Value?md
    m_D = Kilograms(3.342*10**(-27))

    # u_D ($/kg) = 2175 ($/kg) from STARFIRE * 1.12345/0.42273 [GDP IPD ratio for 2019/1980]
    u_D = 2175
    c_f = (float(inputs.basic.n_mod) * inputs.basic.p_nrl * 1e6 * 3600 * 8760
           * u_D * m_D * inputs.basic.plant_availability / (17.58 * 1.6021e-13))

    OUT.C800000 = to_m_usd(c_f)

    OUT.template_file = 'CAS800000_DT.tex'
    OUT.tex_path = 'Modified/' + OUT.template_file
    OUT.replacements = {
        'C800000': round(OUT.C800000, 2),
        'primaryC': inputs.blanket.primary_coolant.display_name,
        'secondaryC': inputs.blanket.secondary_coolant.display_name,
    }
    return OUT