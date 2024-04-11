import math
import matplotlib.pyplot as plt
import numpy as np

from pyfecons import BlanketFirstWall, BlanketType, MagnetMaterialType
from pyfecons.costing.calculations.YuhuHtsCiccExtrapolation import YuhuHtsCiccExtrapolation
from pyfecons.helpers import safe_round
from pyfecons.inputs import (Inputs, Basic, Coils, Magnet, PowerSupplies,
                             DirectEnergyConverter, Installation, FuelHandling)
from pyfecons.data import Data, CAS22, MagnetProperties, PowerTable, VesselCosts, VesselCost
from pyfecons.units import M_USD, Kilometers, Turns, Amperes, Meters2, MA, Meters3, Meters, Kilograms, MW, Count, USD

CAS_220101_MFE_DT_TEX = 'CAS220101_MFE_DT.tex'
CAS_220102_TEX = 'CAS220102.tex'
CAS_220103_MIF_DT_MIRROR = 'CAS220103_MIF_DT_mirror.tex'  # TODO why this mirror file?
CAS_220104_MFE_DT = 'CAS220104_MFE_DT.tex'
CAS_220105_TEX = 'CAS220105.tex'
CAS_220106_MFE_TEX = 'CAS220106_MFE.tex'


def GenerateData(inputs: Inputs, data: Data, figures: dict):
    OUT = data.cas22
    compute_220101_reactor_equipment(inputs, data, figures)
    compute_220102_shield(inputs, data)
    compute_220103_coils(inputs, data)
    compute_220104_supplementary_heating(inputs, data)
    compute_220105_primary_structure(inputs, data)
    compute_220106_vacuum_system(inputs, data, figures)
    compute_220107_power_supplies(inputs.basic, inputs.power_supplies, OUT)
    compute_220108_divertor(inputs, data, figures)
    compute_220109_direct_energy_converter(inputs.direct_energy_converter, OUT)
    compute_220111_installation_costs(inputs.basic, inputs.installation, OUT)
    compute_220119_scheduled_replacement_cost(OUT)
    compute_2201_total(data)
    compute_2202_main_and_secondary_coolant(inputs.basic, data.power_table, OUT)
    compute_2203_auxilary_cooling(inputs.basic, data.power_table, OUT)
    compute_2204_radwaste(data.power_table, OUT)
    compute_2205_fuel_handling_and_storage(inputs.fuel_handling, OUT)
    compute_2206_other_reactor_plant_equipment(data.power_table, OUT)
    compute_2207_instrumentation_and_control(OUT)
    compute_2200_reactor_plant_equipment_total(OUT)


def compute_220101_reactor_equipment(inputs: Inputs, data: Data, figures: dict):
    # Cost Category 22.1.1: Reactor Equipment
    IN = inputs.radial_build
    OUT = data.cas220101
    blanket = inputs.blanket
    materials = inputs.materials

    # Inner radii
    OUT.axis_ir = IN.axis_t
    OUT.plasma_ir = OUT.axis_ir
    OUT.vacuum_ir = IN.plasma_t + OUT.plasma_ir
    OUT.firstwall_ir = IN.vacuum_t + OUT.vacuum_ir
    OUT.blanket1_ir = OUT.firstwall_ir + IN.firstwall_t
    OUT.reflector_ir = OUT.blanket1_ir + IN.blanket1_t
    OUT.ht_shield_ir = OUT.reflector_ir + IN.reflector_t
    OUT.structure_ir = OUT.ht_shield_ir + IN.ht_shield_t
    OUT.gap1_ir = OUT.structure_ir + IN.structure_t
    OUT.vessel_ir = OUT.gap1_ir + IN.gap1_t
    OUT.lt_shield_ir = OUT.vessel_ir + IN.vessel_t  # Moved lt_shield here
    OUT.coil_ir = OUT.lt_shield_ir + IN.lt_shield_t  # Updated coil_ir calculation
    OUT.gap2_ir = OUT.coil_ir + IN.coil_t
    OUT.bioshield_ir = OUT.gap2_ir + IN.gap2_t  # Updated bioshield inner radius

    # Outer radii
    OUT.axis_or = OUT.axis_ir + IN.axis_t
    OUT.plasma_or = OUT.plasma_ir + IN.plasma_t
    OUT.vacuum_or = OUT.vacuum_ir + IN.vacuum_t
    OUT.firstwall_or = OUT.firstwall_ir + IN.firstwall_t
    OUT.blanket1_or = OUT.blanket1_ir + IN.blanket1_t
    OUT.reflector_or = OUT.reflector_ir + IN.reflector_t
    OUT.ht_shield_or = OUT.ht_shield_ir + IN.ht_shield_t
    OUT.structure_or = OUT.structure_ir + IN.structure_t
    OUT.gap1_or = OUT.gap1_ir + IN.gap1_t
    OUT.vessel_or = OUT.vessel_ir + IN.vessel_t
    OUT.lt_shield_or = OUT.lt_shield_ir + IN.lt_shield_t  # Moved lt_shield here
    OUT.coil_or = OUT.coil_ir + IN.coil_t  # Updated coil_or calculation
    OUT.gap2_or = OUT.gap2_ir + IN.gap2_t
    OUT.bioshield_or = OUT.bioshield_ir + IN.bioshield_t  # Updated bioshield outer radius

    def calc_volume_torus(inner, outer):
        return Meters3(2 * np.pi * IN.axis_t * np.pi * (inner + outer) ** 2)

    OUT.axis_vol = 0.0
    OUT.plasma_vol = Meters3(IN.elon * calc_volume_torus(OUT.plasma_ir, IN.plasma_t) - OUT.axis_vol)
    OUT.vacuum_vol = Meters3(IN.elon * calc_volume_torus(OUT.vacuum_ir, IN.vacuum_t)
                             - sum([OUT.plasma_vol, OUT.axis_vol]))
    OUT.firstwall_vol = Meters3(IN.elon * calc_volume_torus(OUT.firstwall_ir, IN.firstwall_t)
                                - sum([OUT.vacuum_vol, OUT.plasma_vol, OUT.axis_vol]))
    OUT.blanket1_vol = Meters3(IN.elon * calc_volume_torus(OUT.blanket1_ir, IN.blanket1_t)
                               - sum([OUT.firstwall_vol, OUT.vacuum_vol, OUT.plasma_vol, OUT.axis_vol]))
    OUT.reflector_vol = Meters3(IN.elon * calc_volume_torus(OUT.reflector_ir, IN.reflector_t)
                                - sum([OUT.blanket1_vol, OUT.firstwall_vol, OUT.vacuum_vol, OUT.plasma_vol,
                                       OUT.axis_vol]))
    OUT.ht_shield_vol = Meters3(IN.elon * calc_volume_torus(OUT.ht_shield_ir, IN.ht_shield_t)
                                - sum([OUT.reflector_vol, OUT.blanket1_vol, OUT.firstwall_vol,
                                       OUT.vacuum_vol, OUT.plasma_vol, OUT.axis_vol]))
    OUT.structure_vol = Meters3(IN.elon * calc_volume_torus(OUT.structure_ir, IN.structure_t)
                                - sum([OUT.ht_shield_vol, OUT.reflector_vol, OUT.blanket1_vol, OUT.firstwall_vol,
                                       OUT.vacuum_vol, OUT.plasma_vol, OUT.axis_vol]))
    OUT.gap1_vol = Meters3(IN.elon * calc_volume_torus(OUT.gap1_ir, IN.gap1_t)
                           - sum([OUT.structure_vol, OUT.ht_shield_vol, OUT.reflector_vol, OUT.blanket1_vol,
                                  OUT.firstwall_vol, OUT.vacuum_vol, OUT.plasma_vol, OUT.axis_vol]))
    OUT.vessel_vol = Meters3(IN.elon * calc_volume_torus(OUT.vessel_ir, IN.vessel_t)
                             - sum([OUT.gap1_vol, OUT.structure_vol, OUT.ht_shield_vol, OUT.reflector_vol,
                                    OUT.blanket1_vol, OUT.firstwall_vol, OUT.vacuum_vol, OUT.plasma_vol, OUT.axis_vol]))
    OUT.lt_shield_vol = Meters3(IN.elon * calc_volume_torus(OUT.lt_shield_ir, IN.lt_shield_t)
                                - sum([OUT.vessel_vol, OUT.gap1_vol, OUT.structure_vol, OUT.ht_shield_vol,
                                       OUT.reflector_vol, OUT.blanket1_vol, OUT.firstwall_vol, OUT.vacuum_vol,
                                       OUT.plasma_vol, OUT.axis_vol]))
    OUT.coil_vol = Meters3(calc_volume_torus(OUT.coil_ir, IN.coil_t) * 0.5)

    def calc_volume_ring(height: Meters, outer: Meters, inner: Meters) -> Meters3:
        return Meters3(height * np.pi * (outer ** 2 - inner ** 2))

    # must be cylindrical in all cases
    OUT.gap2_vol = calc_volume_ring(IN.axis_t, IN.gap2_t + OUT.gap2_ir, OUT.gap2_ir)
    # Updated bioshield volume
    OUT.bioshield_vol = calc_volume_ring(IN.axis_t, IN.bioshield_t + OUT.bioshield_ir, OUT.bioshield_ir)

    # First wall
    if blanket.first_wall == BlanketFirstWall.TUNGSTEN:
        OUT.C22010101 = M_USD(OUT.firstwall_vol * materials.W.rho * materials.W.c_raw * materials.W.m / 1e6)
    elif blanket.first_wall == BlanketFirstWall.LIQUID_LITHIUM:
        OUT.C22010101 = M_USD(OUT.firstwall_vol * materials.Li.rho * materials.Li.c_raw * materials.Li.m / 1e6)
    elif blanket.first_wall == BlanketFirstWall.BERYLLIUM:
        OUT.C22010101 = M_USD(OUT.firstwall_vol * materials.Be.rho * materials.Be.c_raw * materials.Be.m / 1e6)
    elif blanket.first_wall == BlanketFirstWall.FLIBE:
        OUT.C22010101 = M_USD(OUT.firstwall_vol * materials.FliBe.rho * materials.FliBe.c_raw * materials.FliBe.m / 1e6)

    # Blanket
    if blanket.blanket_type == BlanketType.FLOWING_LIQUID_FIRST_WALL:
        OUT.C22010102 = M_USD(OUT.blanket1_vol * materials.Li.rho * materials.Li.c_raw * materials.Li.m / 1e6)
    elif blanket.blanket_type == BlanketType.SOLID_FIRST_WALL_WITH_A_LIQUID_BREEDER:
        OUT.C22010102 = M_USD(OUT.blanket1_vol * materials.Li.rho * materials.Li.c_raw * materials.Li.m / 1e6)
    elif blanket.blanket_type == BlanketType.SOLID_FIRST_WALL_WITH_A_SOLID_BREEDER_LI4SIO4:
        OUT.C22010102 = M_USD(
            OUT.blanket1_vol * materials.Li4SiO4.rho * materials.Li4SiO4.c_raw * materials.Li4SiO4.m / 1e6)
    elif blanket.blanket_type == BlanketType.SOLID_FIRST_WALL_WITH_A_SOLID_BREEDER_LI2TIO3:
        OUT.C22010102 = M_USD(
            OUT.blanket1_vol * materials.Li2TiO3.rho * materials.Li2TiO3.c_raw * materials.Li2TiO3.m / 1e6)
    elif blanket.blanket_type == BlanketType.SOLID_FIRST_WALL_NO_BREEDER_ANEUTRONIC_FUEL:
        OUT.C22010102 = M_USD(0)

    # Total cost of blanket and first wall
    OUT.C220101 = M_USD(OUT.C22010101 + OUT.C22010102)

    # TODO - PLOTTING RADIAL BUILD

    OUT.template_file = CAS_220101_MFE_DT_TEX
    OUT.replacements = {
        'C220101__': str(data.cas220101.C220101),  # TODO - this is not in the template
        'C22010101': str(data.cas220101.C22010101),
        'C22010102': str(data.cas220101.C22010102),

        'primaryC': inputs.blanket.primary_coolant.display_name,
        'secondaryC': inputs.blanket.secondary_coolant.display_name,
        'neutronM': inputs.blanket.neutron_multiplier.display_name,
        'structure1': inputs.blanket.structure.display_name,
        'firstW': inputs.blanket.first_wall.display_name,

        'TH01': round(inputs.radial_build.plasma_t, 1),
        'TH02': round(inputs.radial_build.vacuum_t, 1),
        'TH03': round(inputs.radial_build.firstwall_t, 1),
        'TH04': round(inputs.radial_build.blanket1_t, 1),
        'TH05': round(inputs.radial_build.structure_t, 1),
        'TH06': round(inputs.radial_build.reflector_t, 1),
        'TH07': round(inputs.radial_build.gap1_t, 1),
        'TH08': round(inputs.radial_build.vessel_t, 1),
        'TH09': round(inputs.radial_build.ht_shield_t, 1),
        'TH10': round(inputs.radial_build.lt_shield_t, 1),
        'TH11': round(inputs.radial_build.coil_t, 1),
        'TH12': round(inputs.radial_build.axis_t, 1),
        'TH13': round(inputs.radial_build.gap2_t, 1),
        'TH14': round(inputs.radial_build.bioshield_t, 1),

        'RAD1I': round(data.cas220101.plasma_ir, 1),
        'RAD2I': round(data.cas220101.vacuum_ir, 1),
        'RAD3I': round(data.cas220101.firstwall_ir, 1),
        'RAD4I': round(data.cas220101.blanket1_ir, 1),
        'RAD5I': round(data.cas220101.structure_ir, 1),
        'RAD6I': round(data.cas220101.reflector_ir, 1),
        'RAD7I': round(data.cas220101.gap1_ir, 1),
        'RAD8I': round(data.cas220101.vessel_ir, 1),
        'RAD9I': round(data.cas220101.ht_shield_ir, 1),
        'RAD10I': round(data.cas220101.lt_shield_ir, 1),
        'RAD11I': round(data.cas220101.coil_ir, 1),
        'RAD12I': round(data.cas220101.axis_ir, 1),
        'RAD13I': round(data.cas220101.gap2_ir, 1),
        'RAD14I': round(data.cas220101.bioshield_ir, 1),

        'RAD1O': round(data.cas220101.plasma_or, 1),
        'RAD2O': round(data.cas220101.vacuum_or, 1),
        'RAD3O': round(data.cas220101.firstwall_or, 1),
        'RAD4O': round(data.cas220101.blanket1_or, 1),
        'RAD5O': round(data.cas220101.structure_or, 1),
        'RAD6O': round(data.cas220101.reflector_or, 1),
        'RAD7O': round(data.cas220101.gap1_or, 1),
        'RAD8O': round(data.cas220101.vessel_or, 1),
        'RAD9O': round(data.cas220101.ht_shield_or, 1),
        'RAD10O': round(data.cas220101.lt_shield_or, 1),
        'RAD11O': round(data.cas220101.coil_or, 1),
        'RAD12O': round(data.cas220101.axis_or, 1),
        'RAD13O': round(data.cas220101.gap2_or, 1),
        'RAD14O': round(data.cas220101.bioshield_or, 1),

        'VOL01': round(data.cas220101.plasma_vol, 1),
        'VOL02': round(data.cas220101.vacuum_vol, 1),
        'VOL03': round(data.cas220101.firstwall_vol, 1),
        'VOL04': round(data.cas220101.blanket1_vol, 1),
        'VOL05': round(data.cas220101.structure_vol, 1),
        'VOL06': round(data.cas220101.reflector_vol, 1),
        'VOL07': round(data.cas220101.gap1_vol, 1),
        'VOL08': round(data.cas220101.vessel_vol, 1),
        'VOL09': round(data.cas220101.ht_shield_vol, 1),
        'VOL10': round(data.cas220101.lt_shield_vol, 1),
        'VOL11': round(data.cas220101.coil_vol, 1),
        'VOL12': round(data.cas220101.axis_vol, 1),
        'VOL13': round(data.cas220101.gap2_vol, 1),
        'VOL14': round(data.cas220101.bioshield_vol, 1),
    }


def compute_220102_shield(inputs: Inputs, data: Data):
    # Cost Category 22.1.2: Shield
    OUT = data.cas220102
    cas220101 = data.cas220101
    materials = inputs.materials

    # Define the fractions
    f_SiC = 0.00  # TODO - why is this 0? It invalidates the SiC material contribution
    FPCPPFbLi = 0.1
    f_W = 0.00  # TODO - why is this 0? It invalidates the W material contribution
    f_BFS = 0.9

    # Retrieve the volume of HTS from the reactor_volumes dictionary
    OUT.V_HTS = round(cas220101.ht_shield_vol, 1)

    # Calculate the cost for HTS
    C_HTS = round(OUT.V_HTS * (
            materials.SiC.rho * materials.SiC.c_raw * materials.SiC.m * f_SiC +
            materials.PbLi.rho * materials.PbLi.c * FPCPPFbLi +
            materials.W.rho * materials.W.c_raw * materials.W.m * f_W +
            materials.BFS.rho * materials.BFS.c_raw * materials.BFS.m * f_BFS
    ) / 1e6, 1)

    # Volume of HTShield that is BFS
    V_HTS_BFS = OUT.V_HTS * f_BFS

    # The cost C_22_1_2 is the same as C_HTS
    OUT.C22010201 = M_USD(round(C_HTS, 1))
    OUT.C22010202 = M_USD(cas220101.lt_shield_vol * materials.SS316.c_raw * materials.SS316.m / 1e3)
    OUT.C22010203 = M_USD(cas220101.bioshield_vol * materials.SS316.c_raw * materials.SS316.m / 1e3)
    OUT.C22010204 = M_USD(OUT.C22010203 * 0.1)
    OUT.C220102 = M_USD(OUT.C22010201 + OUT.C22010202 + OUT.C22010203 + OUT.C22010204)

    OUT.template_file = CAS_220102_TEX
    OUT.replacements = {
        'C220102__': round(data.cas220102.C220102),
        'C22010201': round(data.cas220102.C22010201),
        'C22010202': round(data.cas220102.C22010202),
        'C22010203': round(data.cas220102.C22010203),
        'C22010204': round(data.cas220102.C22010204),
        'V220102': round(data.cas220102.V_HTS),  # Missing from CAS220102.tex
        'primaryC': inputs.blanket.primary_coolant.display_name,
        'VOL9': round(data.cas220101.ht_shield_vol),
        'VOL11': round(data.cas220101.lt_shield_vol),  # Missing from CAS220102.tex
    }


def plot_radial_build(IN, figures):
    """
    PLOTTING RADIAL BUILD
    """

    ## The names of the sections

    # Updated order of the sections
    sections = ['Plasma', 'Vacuum', 'First Wall', 'Blanket', 'Reflector', 'HT Shield', 'Structure', 'Gap', 'Vessel',
                'LT Shield', 'Coil', 'Gap', 'Bioshield']

    # The thickness of each section (for stacked bar plot)
    thickness = [IN.plasma_t, IN.vacuum_t, IN.firstwall_t, IN.blanket1_t, IN.reflector_t, IN.ht_shield_t,
                 IN.structure_t, IN.gap1_t, IN.vessel_t, IN.lt_shield_t, IN.coil_t, IN.gap2_t, IN.bioshield_t]

    # Updated colors for each section
    colors = ['purple', 'black', 'lightblue', 'darkblue', 'blue', 'cornflowerblue', 'coral', 'lightgray', 'orange',
              'slateblue', 'green', 'lightgray', 'darkorange']

    # Plotting the stacked bar graph
    fig, ax = plt.subplots(figsize=(18, 3.5))  # Adjust the figsize to get the desired aspect ratio

    # Adding each section to the bar plot
    left = 0  # Initialize left at 0
    for i, (section, thk) in enumerate(zip(sections, thickness)):
        ax.barh('Thickness', thk, left=left, color=colors[i], edgecolor='white', label=section)
        left += thk  # Increment left by the thickness of the current section

    # Setting labels and title
    ax.set_xlabel('Radius (m)')

    # Creating the legend
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

    # Show grid for the x-axis
    ax.xaxis.grid(True)

    # Show the plot
    plt.tight_layout()  # TODO comment or delete
    plt.show()  # TODO comment or delete
    figures["radial_build.pdf"] = fig

    # Export as pdf
    # fig.savefig(os.path.join(figures_directory, 'radial_build.pdf'), bbox_inches='tight')


# Steel thermal conductivity function
def k_steel(t: float) -> float:
    return 10 * t


# Power in from thermal conduction through support
# For 1 coil, assume 20 support beams, 5m length, 0.5m^2 cs area, target temp of 20K, env temp of 300 K
def compute_q_in_struct(coils: Coils, k: float, t_mag: float) -> float:
    # TODO - unsure if we should use t_mag input or keep this as a function parameter. Can we differentiate them?
    return k * coils.beam_cs_area * float(coils.no_beams) / coils.beam_length * (coils.t_env - t_mag) / 1e6


# power in from neutron flux, assume 95% is abosrbed in the blanket
# Neutron heat loading for one coil
def compute_q_in_n(int_coil_area: float, data: Data):
    # surface area  of torus 4 × π^2 × R × r
    return data.power_table.p_neutron * 0.05 * int_coil_area / (
            4 * np.pi ** 2 * (data.cas220101.coil_ir - data.cas220101.axis_ir))


def compute_iter_cost_per_MW(coils):
    # Scaling cooling costs from ITER see Serio, L., ITER Organization and Domestic Agencies and Collaborators, 2010,
    # April. Challenges for cryogenics at ITER. In AIP Conference Proceedings (Vol. 1218, No. 1, pp. 651-662).
    # American Institute of Physics. ITER COP ITERcooling at 4.2 K
    qiter_4k = 47e-3  # 47.1 kW at 4.2 K
    # Calculating ITER cooling at system operating temp in MW
    cost_iter_cooling = 165.1 * 1.43  # 17.65 M USD in 2009 for 20kW at 4.2 K, adjusted to inflation
    learning_credit = 0.5  # ITER system cooling seems unnecessarily high compared with other costings such as STARFIRE, FIRE
    qiter_scaled = MW(qiter_4k / (coils.t_mag / (coils.t_env - 4.2) * coils.c_frac))  # ITER cooling power at T_env
    iter_cost_per_MW = cost_iter_cooling / qiter_scaled * learning_credit
    return iter_cost_per_MW


def compute_magnet_cooling_cost(coils: Coils, magnet: Magnet, data: Data) -> M_USD:
    # Neutron heat loading for one coil
    q_in_n = compute_q_in_n(magnet.dz * abs((magnet.r_centre - magnet.dr / 2)), data)
    # For 1 coil, assume 20 support beams, 5m length, 0.5m^2 cs area, target temp of 20K, env temp of 300 K
    q_in_struct = compute_q_in_struct(coils, k_steel((coils.t_env + magnet.coil_temp) / 2),
                                      (coils.t_env + magnet.coil_temp) / 2)
    q_in = (q_in_struct + q_in_n)  # total input heat for one coil
    return M_USD(q_in * compute_iter_cost_per_MW(coils))


def compute_hts_cicc_auto_magnet_properties(coils: Coils, magnet: Magnet, data: Data) -> MagnetProperties:
    OUT = MagnetProperties()
    OUT.magnet = magnet

    yuhu = YuhuHtsCiccExtrapolation(magnet, True)

    OUT.turns_sc_tot = Turns(yuhu.r_turns * yuhu.z_turns)
    OUT.cable_w = coils.cable_w
    OUT.cable_h = coils.cable_h

    OUT.cs_area = Meters2(yuhu.dr * yuhu.dz)
    OUT.turns_c = Turns(OUT.cs_area / (coils.cable_w * coils.cable_h))
    OUT.turns_scs = Turns(OUT.turns_sc_tot / OUT.turns_c)
    OUT.current_supply = MA(OUT.turns_c * yuhu.cable_current)
    OUT.cable_current = Amperes(yuhu.cable_current)

    OUT.vol_coil = Meters3(OUT.cs_area * 2 * np.pi * magnet.r_centre)
    OUT.tape_length = Kilometers(OUT.turns_sc_tot * magnet.r_centre * 2 * math.pi / 1e3)
    OUT.max_tape_current = Amperes(yuhu.cable_current / OUT.turns_scs)
    OUT.j_tape = coils.j_tape_ybco

    OUT.cost_sc = M_USD(OUT.max_tape_current / 1e3 * OUT.tape_length * 1e3 * coils.m_cost_ybco / 1e6)
    OUT.cost_cu = M_USD(coils.frac_cs_cu_yuhu * coils.m_cost_cu * OUT.vol_coil * coils.cu_density / 1e6)
    OUT.cost_ss = M_USD(coils.frac_cs_ss_yuhu * coils.m_cost_ss * OUT.vol_coil * coils.ss_density / 1e6)
    OUT.cost_i = M_USD(0)
    OUT.tot_mat_cost = M_USD(OUT.cost_sc + OUT.cost_cu + OUT.cost_ss)
    OUT.magnet_cost = M_USD(OUT.tot_mat_cost * coils.mfr_factor)
    OUT.coil_mass = Kilograms((coils.rebco_density * OUT.tape_length * coils.tape_w * coils.tape_t)
                              + (coils.frac_cs_cu_yuhu * OUT.vol_coil * coils.cu_density)
                              + (coils.frac_cs_ss_yuhu * OUT.vol_coil * coils.ss_density))
    OUT.cooling_cost = compute_magnet_cooling_cost(coils, magnet, data)

    OUT.magnet_struct_cost = M_USD(coils.struct_factor * OUT.magnet_cost + OUT.cooling_cost)
    OUT.magnet_total_cost_individual = M_USD(OUT.magnet_cost + OUT.magnet_struct_cost)
    OUT.magnet_total_cost = M_USD(OUT.magnet_total_cost_individual * magnet.coil_count)

    return OUT


def compute_hts_cicc_magnet_properties(coils: Coils, magnet: Magnet, data: Data) -> MagnetProperties:
    OUT = MagnetProperties()
    OUT.magnet = magnet

    OUT.cable_w = coils.cable_w
    OUT.cable_h = coils.cable_h

    OUT.max_tape_current = coils.j_tape_ybco * coils.tape_w * 1e3 * coils.tape_t * 1e3
    OUT.turns_scs = Turns((coils.cable_w * coils.cable_h * coils.frac_cs_sc_yuhu) / (coils.tape_w * coils.tape_t))
    OUT.cable_current = Amperes(OUT.max_tape_current * OUT.turns_scs)

    OUT.cs_area = Meters2(magnet.dr * magnet.dz)
    OUT.turns_c = Turns(OUT.cs_area / (coils.cable_w * coils.cable_h))
    OUT.current_supply = MA(OUT.cable_current * OUT.turns_c)
    OUT.vol_coil = Meters3(OUT.cs_area * 2 * np.pi * magnet.r_centre)

    OUT.turns_sc_tot = Turns(OUT.turns_scs * OUT.turns_c)
    OUT.tape_length = Kilometers(OUT.turns_sc_tot * magnet.r_centre * 2 * math.pi / 1e3)
    OUT.j_tape = coils.j_tape_ybco

    OUT.cost_sc = M_USD(OUT.max_tape_current / 1e3 * OUT.tape_length * 1e3 * coils.m_cost_ybco / 1e6)
    OUT.cost_cu = M_USD(coils.frac_cs_cu_yuhu * coils.m_cost_cu * OUT.vol_coil * coils.cu_density / 1e6)
    OUT.cost_ss = M_USD(coils.frac_cs_ss_yuhu * coils.m_cost_ss * OUT.vol_coil * coils.ss_density / 1e6)
    OUT.cost_i = M_USD(0)
    OUT.tot_mat_cost = M_USD(OUT.cost_sc + OUT.cost_cu + OUT.cost_ss)
    OUT.magnet_cost = M_USD(OUT.tot_mat_cost * coils.mfr_factor)
    OUT.coil_mass = Kilograms((coils.rebco_density * OUT.tape_length * coils.tape_w * coils.tape_t)
                              + (coils.frac_cs_cu_yuhu * OUT.vol_coil * coils.cu_density)
                              + (coils.frac_cs_ss_yuhu * OUT.vol_coil * coils.ss_density))
    OUT.cooling_cost = compute_magnet_cooling_cost(coils, magnet, data)

    OUT.magnet_struct_cost = M_USD(coils.struct_factor * OUT.magnet_cost + OUT.cooling_cost)
    OUT.magnet_total_cost_individual = M_USD(OUT.magnet_cost + OUT.magnet_struct_cost)
    OUT.magnet_total_cost = M_USD(OUT.magnet_total_cost_individual * magnet.coil_count)

    return OUT


def compute_hts_pancake_magnet_properties(coils: Coils, magnet: Magnet, data: Data) -> MagnetProperties:
    OUT = MagnetProperties()
    OUT.magnet = magnet

    # Cables are not used here
    OUT.cable_w = Meters(0)
    OUT.cable_h = Meters(0)

    OUT.max_tape_current = Amperes(coils.j_tape_ybco * coils.tape_w * 1e3 * coils.tape_t * 1e3)
    OUT.cs_area = Meters2(magnet.dr * magnet.dz)
    OUT.turns_scs = Turns((1 - magnet.frac_in) * OUT.cs_area / (coils.tape_w * coils.tape_t))

    # in this case the 'cable' is the entire winding
    OUT.cable_current = Amperes(OUT.max_tape_current * OUT.turns_scs)
    OUT.vol_coil = Meters3(OUT.cs_area * 2 * np.pi * magnet.r_centre)
    OUT.turns_c = Turns(0)
    OUT.turns_sc_tot = OUT.turns_scs
    OUT.current_supply = OUT.cable_current

    OUT.turns_i = Turns(magnet.frac_in * OUT.cs_area / (coils.tape_w * coils.tape_t))
    OUT.no_p = OUT.turns_scs / coils.turns_p

    # TODO are parenthesis correct here in the denominator?
    OUT.vol_i = Meters3(
        OUT.turns_scs * magnet.r_centre * 2 * np.pi / 1e3 * magnet.frac_in * (coils.tape_w * coils.tape_t))
    OUT.tape_length = Kilometers(OUT.turns_sc_tot * magnet.r_centre * 2 * math.pi / 1e3)
    OUT.j_tape = coils.j_tape_ybco

    OUT.cost_sc = M_USD(OUT.max_tape_current / 1e3 * OUT.tape_length * 1e3 * coils.m_cost_ybco / 1e6)
    OUT.cost_i = M_USD(coils.m_cost_i * OUT.vol_i * coils.i_density / 1e6)
    OUT.cost_cu = M_USD(0)
    OUT.cost_ss = M_USD(0)
    OUT.tot_mat_cost = M_USD(OUT.cost_sc + OUT.cost_cu + OUT.cost_ss + OUT.cost_i)
    OUT.magnet_cost = M_USD(OUT.tot_mat_cost * magnet.mfr_factor)
    OUT.coil_mass = Kilograms(coils.rebco_density * OUT.tape_length * coils.tape_w * coils.tape_t
                              + OUT.vol_i * coils.i_density)
    OUT.cooling_cost = compute_magnet_cooling_cost(coils, magnet, data)

    OUT.magnet_struct_cost = M_USD(coils.struct_factor * OUT.magnet_cost + OUT.cooling_cost)
    OUT.magnet_total_cost_individual = M_USD(OUT.magnet_cost + OUT.magnet_struct_cost)
    OUT.magnet_total_cost = M_USD(OUT.magnet_total_cost_individual * magnet.coil_count)

    return OUT


def compute_copper_magnet_properties(coils: Coils, magnet: Magnet, data: Data) -> MagnetProperties:
    OUT = MagnetProperties()
    OUT.magnet = magnet

    OUT.cable_w = Meters(0)  # Cables are not used here
    OUT.cable_h = Meters(0)  # Cables are not used here

    # In this case 'Tape' refers to copper wire AWG 11
    OUT.cs_area = Meters2(magnet.dr * magnet.dz)

    OUT.turns_scs = Turns((1 - magnet.frac_in) * OUT.cs_area / (0.5 * coils.cu_wire_d) ** 2)
    OUT.turns_i = Turns(magnet.frac_in * OUT.cs_area / (0.5 * coils.cu_wire_d) ** 2)

    OUT.vol_coil = Meters3(OUT.cs_area * 2 * np.pi * magnet.r_centre)
    OUT.cu_wire_current = coils.max_cu_current
    OUT.max_tape_current = coils.max_cu_current
    OUT.j_tape = Amperes(coils.max_cu_current / (0.5 * coils.cu_wire_d * 1e3) ** 2)
    OUT.turns_sc_tot = OUT.turns_scs
    OUT.turns_c = Turns(0)
    OUT.cable_current = Amperes(0)
    OUT.tape_length = Kilometers(OUT.turns_scs * magnet.r_centre * 2 * np.pi / 1e3)
    OUT.current_supply = MA(OUT.cu_wire_current * OUT.turns_scs)

    OUT.vol_i = Meters3(magnet.frac_in * OUT.cs_area * magnet.r_centre * 2 * np.pi)
    OUT.cost_sc = M_USD(0)
    # simple volumetric material calc
    OUT.cost_cu = M_USD((OUT.vol_coil - OUT.vol_i) * coils.cu_density * coils.m_cost_cu / 1e6)
    OUT.cost_i = M_USD(coils.m_cost_i * OUT.vol_i * coils.i_density / 1e6)
    OUT.cost_ss = M_USD(0)
    OUT.tot_mat_cost = M_USD(OUT.cost_sc + OUT.cost_cu + OUT.cost_ss + OUT.cost_i)
    OUT.magnet_cost = M_USD(OUT.tot_mat_cost * magnet.mfr_factor)
    OUT.coil_mass = Kilograms(((OUT.vol_coil - OUT.vol_i) * coils.cu_density) + (OUT.vol_i * coils.i_density))
    OUT.cooling_cost = compute_magnet_cooling_cost(coils, magnet, data)

    OUT.magnet_struct_cost = M_USD(coils.struct_factor * OUT.magnet_cost + OUT.cooling_cost)
    OUT.magnet_total_cost_individual = M_USD(OUT.magnet_cost + OUT.magnet_struct_cost)
    OUT.magnet_total_cost = M_USD(OUT.magnet_total_cost_individual * magnet.coil_count)

    return OUT


def compute_magnet_properties(coils: Coils, magnet: Magnet, data: Data) -> MagnetProperties:
    if magnet.material_type == MagnetMaterialType.HTS_CICC:
        if magnet.auto_cicc:
            return compute_hts_cicc_auto_magnet_properties(coils, magnet, data)
        else:
            return compute_hts_cicc_magnet_properties(coils, magnet, data)
    elif magnet.material_type == MagnetMaterialType.HTS_PANCAKE:
        return compute_hts_pancake_magnet_properties(coils, magnet, data)
    elif magnet.material_type == MagnetMaterialType.COPPER:
        return compute_copper_magnet_properties(coils, magnet, data)
    raise f'Unrecognized magnet material type {magnet.material_type}'


def compute_220103_coils(inputs: Inputs, data: Data):
    # Cost Category 22.1.3: Coils
    IN = inputs.coils
    OUT = data.cas220103

    OUT.magnet_properties = [compute_magnet_properties(IN, magnet, data) for magnet in IN.magnets]

    # Assign calculated totals to variables for .tex file
    OUT.C22010301 = M_USD(sum([mag.magnet_total_cost for mag in OUT.tf_coils]))
    OUT.C22010302 = M_USD(sum([mag.magnet_total_cost for mag in OUT.cs_coils]))
    OUT.C22010303 = M_USD(sum([mag.magnet_total_cost for mag in OUT.pf_coils]))
    # Shim coil costs, taken as 5% total primary magnet costs
    OUT.C22010304 = 0.05 * (OUT.C22010301 + OUT.C22010302 + OUT.C22010303)
    OUT.C22010305 = M_USD(sum([mag.magnet_struct_cost for mag in OUT.magnet_properties]))  # Structural cost
    OUT.C22010306 = M_USD(sum([mag.cooling_cost for mag in OUT.magnet_properties]))  # cooling cost
    # Total cost
    OUT.C220103 = M_USD(OUT.C22010301 + OUT.C22010302 + OUT.C22010303 + OUT.C22010304 + OUT.C22010305 + OUT.C22010306)

    # Additional totals and calculations
    OUT.no_pf_coils = Count(sum(magnet.magnet.coil_count for magnet in OUT.pf_coils))
    OUT.no_pf_pairs = Count(OUT.no_pf_coils / 2)

    # TODO verify template substition

    OUT.template_file = CAS_220103_MIF_DT_MIRROR
    OUT.replacements = {
        'C220103__': str(OUT.C220103),
        'C22010301': str(OUT.C22010301),
        'C22010302': str(OUT.C22010302),
        'C22010303': str(OUT.C22010303),
        'C22010304': str(OUT.C22010304),
        'C22010305': str(OUT.C22010305),  # TODO not in template, should it be?
        'C22010306': str(OUT.C22010306),  # TODO not in template, should it be?

        'structFactor': IN.struct_factor,  # TODO not in template, should it be?
        'mcostI': IN.m_cost_ybco,  # TODO why is identical to mCostYBCO, not in template, should it be?
        'nopfcoils': OUT.no_pf_coils,  # TODO not in template, should it be?
        'nopfpairs': OUT.no_pf_pairs,  # TODO not in template, should it be?
        'mCostYBCO': IN.m_cost_ybco,  # TODO not in template, should it be?

        'TABLE_STRUCTURE': ('l' + 'c' * len(OUT.magnet_properties)),
        'TABLE_HEADER_LIST': (" & ".join([f"\\textbf{{{props.magnet.name}}}" for props in OUT.magnet_properties])),
        # TODO fix
        'MAGNET_TYPE_LIST': (
            " & ".join([f"\\textbf{{{props.magnet.material_type.display_name}}}" for props in OUT.magnet_properties])),
        'MAGNET_RADIUS_LIST': (" & ".join([f"{props.magnet.r_centre}" for props in OUT.magnet_properties])),
        'MAGNET_DR_LIST': (" & ".join([f"{props.magnet.dr}" for props in OUT.magnet_properties])),
        'MAGNET_DZ_LIST': (" & ".join([f"{props.magnet.dz}" for props in OUT.magnet_properties])),
        'CURRENT_SUPPLY_LIST': (" & ".join([f"{props.current_supply}" for props in OUT.magnet_properties])),
        # TODO how do we calculate j_cable? Previously this was a magnet property.
        # 'CABLE_CURRENT_DENSITY_LIST': (" & ".join([f"{props.magnet.j_cable}" for props in OUT.magnet_properties])),
        'CONDUCTOR_CURRENT_DENSITY_LIST': (" & ".join([f"{props.j_tape}" for props in OUT.magnet_properties])),
        'CABLE_WIDTH_LIST': (" & ".join([f"{props.cable_w}" for props in OUT.magnet_properties])),
        'CABLE_HEIGHT_LIST': (" & ".join([f"{props.cable_h}" for props in OUT.magnet_properties])),
        'TOTAL_VOLUME_LIST': (" & ".join([f"{props.vol_coil}" for props in OUT.magnet_properties])),
        'CROSS_SECTIONAL_AREA_LIST': (" & ".join([f"{props.cs_area}" for props in OUT.magnet_properties])),
        'TURN_INSULATION_FRACTION_LIST': (" & ".join([f"{props.magnet.frac_in}" for props in OUT.magnet_properties])),
        'CABLE_TURNS_LIST': (" & ".join([f"{props.turns_c}" for props in OUT.magnet_properties])),
        'TOTAL_TURNS_OF_CONDUCTOR_LIST': (" & ".join([f"{props.turns_scs}" for props in OUT.magnet_properties])),
        'LENGTH_OF_CONDUCTOR_LIST': (" & ".join([f"{props.tape_length}" for props in OUT.magnet_properties])),
        'CURRENT_PER_CONDUCTOR_LIST': (" & ".join([f"{props.max_tape_current}" for props in OUT.magnet_properties])),
        'COST_OF_SC_LIST': (" & ".join([f"{props.cost_sc}" for props in OUT.magnet_properties])),
        'COST_OF_COPPER_LIST': (" & ".join([f"{props.cost_cu}" for props in OUT.magnet_properties])),
        'COST_OF_TURN_INSULATION_LIST': (" & ".join([f"{props.cost_i}" for props in OUT.magnet_properties])),
        'COST_OF_SS_LIST': (" & ".join([f"{props.cost_ss}" for props in OUT.magnet_properties])),
        'TOTAL_MATERIAL_COST_LIST': (" & ".join([f"{props.tot_mat_cost}" for props in OUT.magnet_properties])),
        'MANUFACTURING_FACTOR_LIST': (" & ".join([f"{IN.mfr_factor}" for _ in OUT.magnet_properties])),
        'STRUCTURAL_COST_LIST': (" & ".join([f"{props.magnet_struct_cost}" for props in OUT.magnet_properties])),
        'NUMBER_COILS_LIST': (" & ".join([f"{props.magnet.coil_count}" for props in OUT.magnet_properties])),
        'QUANTITY_LIST': (" & ".join([f"{props.magnet.coil_count}" for props in OUT.magnet_properties])),
        'MAGNET_COST_LIST': (" & ".join([f"{props.magnet_cost}" for props in OUT.magnet_properties])),
        'MAGNET_TOTAL_COST_INDIVIDUAL_LIST': (
            " & ".join([f"{props.magnet_total_cost_individual}" for props in OUT.magnet_properties])),
        'MAGNET_TOTAL_COST_LIST': (
            " & ".join([f"{props.magnet_total_cost_individual}" for props in OUT.magnet_properties])),
    }


def compute_220104_supplementary_heating(inputs: Inputs, data: Data):
    # 22.1.4 Supplementary heating
    IN = inputs.supplementary_heating
    OUT = data.cas220104
    OUT.C22010401 = M_USD(IN.average_nbi.cost_2023 * IN.nbi_power)
    OUT.C22010402 = M_USD(IN.average_icrf.cost_2023 * IN.icrf_power)
    OUT.C220104 = M_USD(OUT.C22010401 + OUT.C22010402)

    heating_table_rows = "\n".join([
        f"        {ref.name} & {ref.type} & {round(ref.power, 2)} " +
        f"& {safe_round(ref.cost_2009, 2)} & {round(ref.cost_2023, 2)} \\\\"
        for ref in IN.heating_refs()
    ])

    OUT.template_file = CAS_220104_MFE_DT
    OUT.replacements = {
        'C22010401': str(round(OUT.C22010401, 3)),
        'C22010402': str(round(OUT.C22010402, 3)),
        'C220104__': str(round(OUT.C220104, 3)),
        'NBIPOWER': str(round(IN.nbi_power, 3)),
        'ICRFPOWER': str(round(IN.icrf_power, 3)),
        'HEATING_TABLE_ROWS': heating_table_rows,
    }


def compute_220105_primary_structure(inputs: Inputs, data: Data):
    # 22.1.5 primary structure
    IN = inputs.primary_structure
    OUT = data.cas220105

    # lambda function to compute scaled costs in these calculations
    scaled_cost = lambda cost: cost * data.power_table.p_et / 1000 * IN.learning_credit

    # standard engineering costs
    OUT.C22010501 = M_USD(scaled_cost(IN.analyze_costs)
                          + scaled_cost(IN.unit1_seismic_costs)
                          + scaled_cost(IN.reg_rev_costs))

    # standard fabrication costs
    OUT.C22010502 = M_USD(scaled_cost(IN.unit1_fab_costs) + scaled_cost(IN.unit10_fabcosts))

    # add system PGA costs
    pga_costs = IN.get_pga_costs()
    OUT.C22010501 = M_USD(OUT.C22010501 + pga_costs.eng_costs)
    OUT.C22010502 = M_USD(OUT.C22010502 + pga_costs.fab_costs)

    # total cost calculation
    OUT.C220105 = M_USD(OUT.C22010501 + OUT.C22010502)
    OUT.template_file = CAS_220105_TEX
    OUT.replacements = {
        'C22010501': str(OUT.C22010501),
        'C22010502': str(OUT.C22010502),
        'C22010500': str(OUT.C220105),
        'systPGA': str(IN.syst_pga.value),
        'PNRL': str(inputs.basic.p_nrl)
    }


def compute_220106_vacuum_system(inputs: Inputs, data: Data, figures: dict):
    # 22.1.6 Vacuum system
    OUT = data.cas220106
    IN = inputs.vacuum_system
    build = data.cas220101

    # 22.1.6.1 Vacuum Vessel
    # from radial build
    syst_spool_ir = build.axis_ir - (build.vessel_ir - build.axis_ir) * 0.5  # Spool inner radius (goes around CS)
    syst_doors_ir = build.vessel_ir  # doors inner radius (goes within TF)
    syst_height = inputs.radial_build.elon * build.vessel_vol / (np.pi * build.vessel_ir ** 2)  # System height

    # Cost reference from: Lester M. Waganer et al., 2006, Fusion Engineering and Design
    # TODO figure out why intellij is giving warnings for these assignments
    OUT.vessel_costs = VesselCosts(
        spool_assembly=VesselCost(name="Spool assembly", total_mass=Kilograms(136043), material_cost=USD(49430),
                                  fabrication_cost=USD(2614897), total_cost=USD(2800370)),
        removable_doors=VesselCost(name="Removable doors", total_mass=Kilograms(211328), material_cost=USD(859863),
                                   fabrication_cost=USD(6241880), total_cost=USD(7313071)),
        door_frames=VesselCost(name="Doorframes", total_mass=Kilograms(53632), material_cost=USD(356555),
                               fabrication_cost=USD(2736320), total_cost=USD(3146507)),
        port_enclosures=VesselCost(name="Port enclosures", total_mass=Kilograms(712448), material_cost=USD(2020698),
                                   fabrication_cost=USD(14309096), total_cost=USD(17042242)),
        total=VesselCost(name="Total"),
        contingency=VesselCost(name="Contingency (20%)"),
        prime_contractor_fee=VesselCost(name="Prime contractor fee (12%)"),
        total_subsystem_cost=VesselCost(name="Total subsystem cost")
    )

    for cost in [OUT.vessel_costs.spool_assembly, OUT.vessel_costs.removable_doors,
                 OUT.vessel_costs.door_frames, OUT.vessel_costs.port_enclosures]:
        geometry_factor = (syst_spool_ir / IN.spool_ir) * (syst_height / IN.spool_height) \
            if cost.name == "Spool assembly" \
            else (syst_doors_ir / IN.door_irb) * (syst_height / IN.spool_height)
        cost.total_mass = cost.total_mass * geometry_factor

        # Scaling costs based on new mass
        if cost.total_mass > 0:
            # New cost based on per kg rate, applying learning credit and inflation
            cost.material_cost = cost.material_cost * geometry_factor * IN.learning_credit * IN.inflation_factor
            cost.fabrication_cost = cost.fabrication_cost * geometry_factor * IN.learning_credit * IN.inflation_factor

        # Updating total cost after scaling other costs
        cost.total_cost = cost.material_cost + cost.fabrication_cost

        # Summing updated values to "Total"
        OUT.vessel_costs.total.total_mass += cost.total_mass
        OUT.vessel_costs.total.material_cost += cost.material_cost
        OUT.vessel_costs.total.fabrication_cost += cost.fabrication_cost
        OUT.vessel_costs.total.total_cost += cost.total_mass

    # Calculate new contingency and prime contractor fee based on updated total cost
    total_cost = OUT.vessel_costs.total.total_cost
    OUT.vessel_costs.contingency.total_cost = total_cost * 0.20  # 20%
    OUT.vessel_costs.prime_contractor_fee.total_cost = total_cost * 0.12  # 12%

    # Update the total subsystem cost
    OUT.vessel_costs.total_subsystem_cost.total_cost = (total_cost
                                                        + OUT.vessel_costs.contingency.total_cost
                                                        + OUT.vessel_costs.prime_contractor_fee.total_cost)

    # Calculate mass and cost
    OUT.massstruct = OUT.vessel_costs.total.total_mass
    OUT.vesvol = np.pi * (syst_doors_ir ** 2 - syst_spool_ir ** 2) * syst_height
    OUT.C22010601 = M_USD(OUT.vessel_costs.total_subsystem_cost.total_cost / 1e6)

    # Now calculated in C22010306
    # COOLING 22.1.6.2
    OUT.C22010602 = M_USD(0)

    # VACUUM PUMPING 22.1.6.3
    # Number of vacuum pumps required to pump the full vacuum in 1 second
    no_vpumps = int(OUT.vesvol / IN.vpump_cap)
    OUT.C22010603 = M_USD(no_vpumps * IN.cost_pump / 1e6)

    # ROUGHING PUMP 22.1.6.4
    # from STARFIRE, only 1 needed
    # TODO where do these constants come from?
    OUT.C22010604 = M_USD(120000 * 2.85 / 1e6)

    # TODO review these numbers because they seem really low, maybe some units are missing?
    OUT.C220106 = M_USD(OUT.C22010601 + OUT.C22010602 + OUT.C22010603 + OUT.C22010604)
    OUT.template_file = CAS_220106_MFE_TEX
    OUT.replacements = {
        'C22010601': round(OUT.C22010601),
        'C22010602': round(OUT.C22010601),
        'C22010603': round(OUT.C22010603),
        'C22010604': round(OUT.C22010604),
        'C22010600': round(OUT.C220106),
        'vesvol': round(OUT.vesvol),
        'massstruct': round(OUT.massstruct),
        'vesmatcost': round(OUT.vessel_costs.total.material_cost / 1e6, 1),
        # TODO we have materialvolume in the template but no longer compute it in the code
    }


def compute_220107_power_supplies(basic: Basic, power_supplies: PowerSupplies, OUT: CAS22):
    # Cost Category 22.1.7 Power supplies
    # Scaled relative to ITER for a 500MW fusion power system
    cost_in_kiua = 269.6 * basic.p_nrl / 500 * power_supplies.learning_credit
    OUT.C220107 = M_USD(cost_in_kiua * 2)  # assuming 1kIUA equals $2 M
    return OUT


def compute_220108_divertor(inputs: Inputs, data: Data, figures: dict) -> CAS22:
    OUT = data.cas22
    # 22.1.8 Divertor
    # Simple volumetric calculation based on reactor geometry, user input, and tungsten material
    # properties (see "materials" dictionary)
    OUT.divertor_maj_rad = Meters(data.cas220101.coil_ir - data.cas220101.axis_ir)
    OUT.divertor_min_rad = Meters(data.cas220101.firstwall_ir - data.cas220101.axis_ir)
    OUT.divertor_thickness_z = Meters(0.2)
    OUT.divertor_thickness_r = Meters(OUT.divertor_min_rad * 2)
    OUT.divertor_material = inputs.materials.W  # Tungsten

    # volume of the divertor based on TF coil radius
    OUT.divertor_vol = Meters3(((OUT.divertor_maj_rad + OUT.divertor_thickness_r) ** 2
                                - (OUT.divertor_maj_rad - OUT.divertor_thickness_r) ** 2)
                               * np.pi * OUT.divertor_thickness_z)
    OUT.divertor_mass = Kilograms(OUT.divertor_vol * OUT.divertor_material.rho)
    OUT.divertor_mat_cost = M_USD(OUT.divertor_mass * OUT.divertor_material.c_raw)
    OUT.divertor_cost = M_USD(OUT.divertor_mat_cost * OUT.divertor_material.m)
    OUT.C220108 = M_USD(OUT.divertor_cost / 1e6)
    return OUT


def compute_220109_direct_energy_converter(direct_energy_converter: DirectEnergyConverter, OUT: CAS22) -> CAS22:
    # 22.1.9 Direct Energy Converter
    # lambda function to compute scaled costs in these calculations
    scaled_cost = lambda cost: (cost * direct_energy_converter.system_power
                                * (1 / math.sqrt(direct_energy_converter.flux_limit)) ** 3)
    OUT.scaled_direct_energy_costs = {key: M_USD(scaled_cost(value)) for key, value in
                                      direct_energy_converter.costs.items()}
    OUT.C220109 = M_USD(sum(OUT.scaled_direct_energy_costs.values()))
    return OUT


def compute_220111_installation_costs(basic: Basic, installation: Installation, OUT: CAS22) -> CAS22:
    # Cost Category 22.1.11 Installation costs
    construction_worker = 20 * installation.r / 4
    C_22_1_11_in = installation.nmod * basic.construction_time * (installation.labor_rate * 20 * 300)
    C_22_1_11_1_in = installation.nmod * (
            (installation.labor_rate * 200 * construction_worker) + 0)  # 22.1 first wall blanket
    C_22_1_11_2_in = installation.nmod * ((installation.labor_rate * 150 * construction_worker) + 0)  # 22.2 shield
    C_22_1_11_3_in = installation.nmod * ((installation.labor_rate * 100 * construction_worker) + 0)  # coils
    C_22_1_11_4_in = installation.nmod * (
            (installation.labor_rate * 30 * construction_worker) + 0)  # supplementary heating
    C_22_1_11_5_in = installation.nmod * ((installation.labor_rate * 60 * construction_worker) + 0)  # primary structure
    C_22_1_11_6_in = installation.nmod * ((installation.labor_rate * 200 * construction_worker) + 0)  # vacuum system
    C_22_1_11_7_in = installation.nmod * ((installation.labor_rate * 400 * construction_worker) + 0)  # power supplies
    C_22_1_11_8_in = 0  # guns
    C_22_1_11_9_in = installation.nmod * (
            (installation.labor_rate * 200 * construction_worker) + 0)  # direct energy converter
    C_22_1_11_10_in = 0  # ECRH

    # Total cost calculations
    OUT.C220111 = M_USD(
        C_22_1_11_in + C_22_1_11_1_in + C_22_1_11_2_in + C_22_1_11_3_in + C_22_1_11_4_in + C_22_1_11_5_in
        + C_22_1_11_6_in + C_22_1_11_7_in + C_22_1_11_8_in + C_22_1_11_9_in + C_22_1_11_10_in)
    return OUT


def compute_220119_scheduled_replacement_cost(OUT: CAS22) -> CAS22:
    # Cost category 22.1.19 Scheduled Replacement Cost
    OUT.C220119 = M_USD(0)
    return OUT


def compute_2201_total(data: Data):
    OUT = data.cas22
    # Cost category 22.1 total
    OUT.C220100 = M_USD(data.cas220101.C220101 + data.cas220102.C220102 + data.cas220103.C220103
                        + data.cas220104.C220104 + data.cas220105.C220105 + data.cas220106.C220106 + OUT.C220107
                        + OUT.C220111)


def compute_2202_main_and_secondary_coolant(basic: Basic, power_table: PowerTable, OUT: CAS22) -> CAS22:
    # TODO - audit this function since there is lots of commented code
    # MAIN AND SECONDARY COOLANT Cost Category 22.2

    # Li(f), PbLi, He:                %Primary coolant(i):
    # C_22_2_1  = 233.9 * (PTH/3500)^0.55

    # am assuming a linear scaling	%Li(f), PbLi, He:
    # C220201  = 268.5  * (float(basic.n_mod) * power_table.p_th / 3500) * 1.71

    # Primary coolant(i):  1.85 is due to inflation%the CPI scaling of 1.71 comes from:
    # https://www.bls.gov/data/inflation_calculator.htm scaled relative to 1992 dollars (despite 2003 publication date)
    # this is the Sheffield cost for a 1GWe system
    OUT.C220201 = M_USD(166 * (float(basic.n_mod) * power_table.p_net / 1000))

    # OC, H2O(g)
    # C_22_2_1  = 75.0 * (PTH/3500)^0.55
    # Intermediate coolant system
    OUT.C220202 = M_USD(40.6 * (power_table.p_th / 3500) ** 0.55)

    OUT.C220203 = M_USD(0)
    # Secondary coolant system
    # 75.0 * (PTH/3500)^0.55

    # Main heat-transfer system (NSSS)
    OUT.C220200 = M_USD(OUT.C220201 + OUT.C220202 + OUT.C220203)
    return OUT


def compute_2203_auxilary_cooling(basic: Basic, power_table: PowerTable, OUT: CAS22) -> CAS22:
    # Cost Category 22.3  Auxiliary cooling
    # the CPI scaling of 2.02 comes from: https://www.bls.gov/data/inflation_calculator.htm
    # scaled relative to 1992 dollars (despite 2003 publication date)
    OUT.C220300 = M_USD(1.10 * 1e-3 * float(basic.n_mod) * power_table.p_th * 2.02)
    return OUT


def compute_2204_radwaste(power_table: PowerTable, OUT: CAS22) -> CAS22:
    # Cost Category 22.4 Radwaste
    # Radioactive waste treatment
    # the CPI scaling of 1.96 comes from: https://www.bls.gov/data/inflation_calculator.htm
    # scaled relative to 1992 dollars (despite 2003 publication date)
    OUT.C220400 = M_USD(1.96 * 1e-3 * power_table.p_th * 2.02)
    return OUT


def compute_2205_fuel_handling_and_storage(fuel_handling: FuelHandling, OUT: CAS22) -> CAS22:
    # Cost Category 22.5 Fuel Handling and Storage
    OUT.C2205010ITER = M_USD(20.465 * fuel_handling.inflation)
    OUT.C2205020ITER = M_USD(7 * fuel_handling.inflation)
    OUT.C2205030ITER = M_USD(22.511 * fuel_handling.inflation)
    OUT.C2205040ITER = M_USD(9.76 * fuel_handling.inflation)
    OUT.C2205050ITER = M_USD(22.826 * fuel_handling.inflation)
    OUT.C2205060ITER = M_USD(47.542 * fuel_handling.inflation)
    # ITER inflation cost
    OUT.C22050ITER = M_USD(OUT.C2205010ITER + OUT.C2205020ITER + OUT.C2205030ITER
                           + OUT.C2205040ITER + OUT.C2205050ITER + OUT.C2205060ITER)

    OUT.C220501 = M_USD(OUT.C2205010ITER * fuel_handling.learning_tenth_of_a_kind)
    OUT.C220502 = M_USD(OUT.C2205020ITER * fuel_handling.learning_tenth_of_a_kind)
    OUT.C220503 = M_USD(OUT.C2205030ITER * fuel_handling.learning_tenth_of_a_kind)
    OUT.C220504 = M_USD(OUT.C2205040ITER * fuel_handling.learning_tenth_of_a_kind)
    OUT.C220505 = M_USD(OUT.C2205050ITER * fuel_handling.learning_tenth_of_a_kind)
    OUT.C220506 = M_USD(OUT.C2205060ITER * fuel_handling.learning_tenth_of_a_kind)
    # ITER inflation cost
    OUT.C220500 = M_USD(OUT.C220501 + OUT.C220502 + OUT.C220503 + OUT.C220504 + OUT.C220505 + OUT.C220506)

    return OUT


def compute_2206_other_reactor_plant_equipment(power_table: PowerTable, OUT: CAS22):
    # Cost Category 22.6 Other Reactor Plant Equipment
    # From Waganer
    OUT.C220600 = M_USD(11.5 * (power_table.p_net / 1000) ** (0.8))
    return OUT


def compute_2207_instrumentation_and_control(OUT: CAS22) -> CAS22:
    # Cost Category 22.7 Instrumentation and Control
    OUT.C220700 = M_USD(85)
    return OUT


def compute_2200_reactor_plant_equipment_total(OUT: CAS22) -> CAS22:
    # Reactor Plant Equipment (RPE) total
    OUT.C220000 = M_USD(OUT.C220100 + OUT.C220200 + OUT.C220300 + OUT.C220400 + OUT.C220500 + OUT.C220600 + OUT.C220700)
    return OUT
