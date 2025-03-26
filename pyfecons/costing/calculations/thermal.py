import numpy as np
from pyfecons.costing.calculations.conversions import w_to_mw
from pyfecons.costing.accounting.power_table import PowerTable
from pyfecons.enums import MagnetType
from pyfecons.inputs.coils import Coils
from pyfecons.inputs.magnet import Magnet
from pyfecons.inputs.radial_build import RadialBuild
from pyfecons.units import MW


# Steel thermal conductivity function
def k_steel(t: float) -> float:
    return 10 * t


# Power in from thermal conduction through support
# For 1 coil, assume 20 support beams, 5m length, 0.5m^2 cs area, target temp of 20K, env temp of 300 K
def compute_q_in_struct(coils: Coils, k: float, t_op: float) -> MW:
    # TODO - unsure if we should use t_op input or keep this as a function parameter. Can we differentiate them?
    return w_to_mw(
        k
        * coils.beam_cs_area
        * float(coils.no_beams)
        / coils.beam_length
        * (coils.t_env - t_op)
    )


def compute_q_in_n(magnet: Magnet, power_table: PowerTable, radial_build: RadialBuild):
    # TODO clarify it's not the formula in collab
    # load_area = magnet.r_center - radial_build.axis_t
    load_area = magnet.dz * abs((magnet.r_centre - magnet.dr / 2))
    q_n_per_coil = compute_q_in_n_per_coil(
        load_area, power_table.p_neutron, radial_build.axis_t, magnet.dz
    )
    if magnet.type == MagnetType.TF:
        q_n_per_coil = q_n_per_coil * magnet.coil_count
    return q_n_per_coil


# power in from neutron flux, assume 95% is abosrbed in the blanket
# Neutron heat loading for one coil
def compute_q_in_n_per_coil(
    load_area: float, p_neutron: float, maj_r: float, min_r: float
) -> float:
    # surface area of torus 4 × π^2 × R × r
    return p_neutron * 0.05 * load_area / (4 * np.pi**2 * (maj_r - min_r))


def compute_iter_cost_per_MW(coils):
    # Scaling cooling costs from ITER see Serio, L., ITER Organization and Domestic Agencies and Collaborators, 2010,
    # April. Challenges for cryogenics at ITER. In AIP Conference Proceedings (Vol. 1218, No. 1, pp. 651-662).
    # American Institute of Physics. ITER COP ITERcooling at 4.2 K
    qiter_4k = 47e-3  # 47.1 kW at 4.2 K
    # Calculating ITER cooling at system operating temp in MW
    cost_iter_cooling = (
        165.1 * 1.43
    )  # 17.65 M USD in 2009 for 20kW at 4.2 K, adjusted to inflation
    learning_credit = 0.5  # ITER system cooling seems unnecessarily high compared with other costings such as STARFIRE, FIRE
    qiter_scaled = MW(
        qiter_4k / (coils.t_op / (coils.t_env - 4.2) * coils.c_frac)
    )  # ITER cooling power at T_env
    iter_cost_per_MW = cost_iter_cooling / qiter_scaled * learning_credit
    return iter_cost_per_MW
