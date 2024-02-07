import math
import matplotlib.pyplot as plt
import numpy as np

from pyfecons.inputs import Inputs, Basic, RadialBuild, Coils, Magnet
from pyfecons.data import Data, CAS22, MagnetProperties
from pyfecons.materials import Materials
from pyfecons.units import Currency, Kilometers, Turns, Amperes, Meters2, MA, Meters3


def GenerateData(inputs: Inputs, data: Data, figures: dict):
    OUT = data.cas22
    compute_220101_reactor_equipment(inputs.basic, inputs.radial_build, inputs.materials, OUT)
    compute_220102_shield(inputs.materials, OUT)
    compute_220103_coils(inputs.coils, OUT)


def compute_220101_reactor_equipment(BASIC: Basic, RADIAL_BUILD: RadialBuild, MATERIALS: Materials, OUT: CAS22):
    # Cost Category 22.1.1: Reactor Equipment

    # Inner radii
    OUT.axis_ir = RADIAL_BUILD.axis_t
    OUT.plasma_ir = RADIAL_BUILD.plasma_t
    OUT.vacuum_ir = RADIAL_BUILD.vacuum_t + RADIAL_BUILD.plasma_t
    OUT.firstwall_ir = RADIAL_BUILD.vacuum_t + OUT.vacuum_ir
    OUT.blanket1_ir = OUT.firstwall_ir + RADIAL_BUILD.firstwall_t
    OUT.reflector_ir = OUT.blanket1_ir + RADIAL_BUILD.blanket1_t
    OUT.ht_shield_ir = OUT.reflector_ir + RADIAL_BUILD.reflector_t
    OUT.structure_ir = OUT.ht_shield_ir + RADIAL_BUILD.ht_shield_t
    OUT.gap1_ir = OUT.structure_ir + RADIAL_BUILD.structure_t
    OUT.vessel_ir = OUT.gap1_ir + RADIAL_BUILD.gap1_t
    OUT.lt_shield_ir = OUT.vessel_ir + RADIAL_BUILD.vessel_t  # Moved lt_shield here
    OUT.coil_ir = OUT.lt_shield_ir + RADIAL_BUILD.lt_shield_t  # Updated coil_ir calculation
    OUT.gap2_ir = OUT.coil_ir + RADIAL_BUILD.coil_t
    OUT.bioshield_ir = OUT.gap2_ir + RADIAL_BUILD.gap2_t  # Updated bioshield inner radius
    # Outer radii
    OUT.axis_or = OUT.axis_ir + RADIAL_BUILD.axis_t
    OUT.plasma_or = OUT.plasma_ir + RADIAL_BUILD.plasma_t
    OUT.vacuum_or = OUT.vacuum_ir + RADIAL_BUILD.vacuum_t
    OUT.firstwall_or = OUT.firstwall_ir + RADIAL_BUILD.firstwall_t
    OUT.blanket1_or = OUT.blanket1_ir + RADIAL_BUILD.blanket1_t
    OUT.reflector_or = OUT.reflector_ir + RADIAL_BUILD.reflector_t
    OUT.ht_shield_or = OUT.ht_shield_ir + RADIAL_BUILD.ht_shield_t
    OUT.structure_or = OUT.structure_ir + RADIAL_BUILD.structure_t
    OUT.gap1_or = OUT.gap1_ir + RADIAL_BUILD.gap1_t
    OUT.vessel_or = OUT.vessel_ir + RADIAL_BUILD.vessel_t
    OUT.lt_shield_or = OUT.lt_shield_ir + RADIAL_BUILD.lt_shield_t  # Moved lt_shield here
    OUT.coil_or = OUT.coil_ir + RADIAL_BUILD.coil_t  # Updated coil_or calculation
    OUT.gap2_or = OUT.gap2_ir + RADIAL_BUILD.gap2_t
    OUT.bioshield_or = OUT.bioshield_ir + RADIAL_BUILD.bioshield_t  # Updated bioshield outer radius

    def calc_volume(inner, outer):
        return RADIAL_BUILD.chamber_length * math.pi * (outer ** 2 - inner ** 2)

    # Volumes for cylinder
    OUT.axis_vol = calc_volume(OUT.axis_ir, OUT.axis_or)
    OUT.plasma_vol = calc_volume(OUT.plasma_ir, OUT.plasma_or)
    OUT.vacuum_vol = calc_volume(OUT.vacuum_ir, OUT.vacuum_or)
    OUT.firstwall_vol = calc_volume(OUT.firstwall_ir, OUT.firstwall_or)
    OUT.blanket1_vol = calc_volume(OUT.blanket1_ir, OUT.blanket1_or)
    OUT.reflector_vol = calc_volume(OUT.reflector_ir, OUT.reflector_or)
    OUT.ht_shield_vol = calc_volume(OUT.ht_shield_ir, OUT.ht_shield_or)
    OUT.structure_vol = calc_volume(OUT.structure_ir, OUT.structure_or)
    OUT.gap1_vol = calc_volume(OUT.gap1_ir, OUT.gap1_or)
    OUT.vessel_vol = calc_volume(OUT.vessel_ir, OUT.vessel_or)
    OUT.lt_shield_vol = calc_volume(OUT.lt_shield_ir, OUT.lt_shield_or)  # Moved lt_shield volume here
    OUT.coil_vol = calc_volume(OUT.coil_ir, OUT.coil_or) * (9 * 0.779) / 40  # Updated coil volume calculation
    OUT.gap2_vol = calc_volume(OUT.gap2_ir, OUT.gap2_or)
    OUT.bioshield_vol = calc_volume(OUT.bioshield_ir, OUT.bioshield_or)  # Updated bioshield volume

    # Cost calc 1
    # Define the values
    f_W = 1
    C_OFW = 0
    M_OFW = 0

    # Blanket is rotating vortex of PbLi
    FPCPPFbLi = 0.9
    f_FS = 0.1

    # Cost of blanket
    C_OBI_PbLi = OUT.blanket1_vol * (MATERIALS.PbLi.rho * MATERIALS.PbLi.c * FPCPPFbLi)
    C_OBI_FS = OUT.blanket1_vol * (MATERIALS.FS.rho * MATERIALS.FS.c_raw * f_FS)

    # Total heat capacity of OBI
    C_OBI = C_OBI_FS + C_OBI_PbLi

    # Calculate C_22_1_1
    OUT.C220101 = BASIC.am * float(BASIC.n_mod) * (C_OFW + C_OBI) / 1e6  # First Wall/Blanket/reflector

    # plot_radial_build(RADIAL_BUILD, figures)


def compute_220102_shield(MATERIALS: Materials, OUT: CAS22):
    # Cost Category 22.1.2: Shield
    # Define the fractions
    f_SiC = 0.00  # TODO - why is this 0? It invalidates the SiC material contribution
    FPCPPFbLi = 0.1
    f_W = 0.00  # TODO - why is this 0? It invalidates the W material contribution
    f_BFS = 0.9
    # TODO - what is this line?
    reactor = 'CATF'
    # Retrieve the volume of HTS from the reactor_volumes dictionary
    # V_HTS = volumes["V_HTS"]
    OUT.V_HTS = round(OUT.ht_shield_vol, 1)
    # Calculate the cost for HTS
    C_HTS = round(OUT.V_HTS * (
            MATERIALS.SiC.rho * MATERIALS.SiC.c_raw * MATERIALS.SiC.m * f_SiC +
            MATERIALS.PbLi.rho * MATERIALS.PbLi.c * FPCPPFbLi +
            MATERIALS.W.rho * MATERIALS.W.c_raw * MATERIALS.W.m * f_W +
            MATERIALS.BFS.rho * MATERIALS.BFS.c_raw * MATERIALS.BFS.m * f_BFS
    ) / 1e6, 1)
    # Volume of HTShield that is BFS
    V_HTS_BFS = OUT.V_HTS * f_BFS
    # The cost C_22_1_2 is the same as C_HTS
    OUT.C22010201 = round(C_HTS, 1)
    OUT.C22010202 = OUT.lt_shield_vol * MATERIALS.SS316.c_raw * MATERIALS.SS316.m / 1e3
    OUT.C22010203 = OUT.bioshield_vol * MATERIALS.SS316.c_raw * MATERIALS.SS316.m / 1e3
    OUT.C22010204 = OUT.C22010203 * 0.1
    OUT.C220102 = OUT.C22010201 + OUT.C22010202 + OUT.C22010203 + OUT.C22010204


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


def compute_magnet_properties(COILS: Coils, MAGNET: Magnet):
    OUT = MagnetProperties(magnet=MAGNET)

    # Calculate maximum current based on tape dimensions and current density
    max_tape_current = COILS.j_tape * COILS.tape_w * 1e3 * COILS.tape_t * 1e3  # Current in A
    OUT.tape_current = Amperes(max_tape_current)
    turns_scs = (COILS.cable_w * COILS.cable_h * COILS.frac_cs_sc_yuhu) / (COILS.tape_w * COILS.tape_t)
    OUT.cable_current = Amperes(max_tape_current * turns_scs)

    OUT.cs_area = Meters2(MAGNET.dr * MAGNET.dz)
    OUT.turns_c = Turns(OUT.cs_area / (COILS.cable_w * COILS.cable_h))
    OUT.current_supply = MA(OUT.cable_current * OUT.turns_c)
    OUT.vol_coil = Meters3(OUT.cs_area * 2 * np.pi * MAGNET.r_centre)

    OUT.turns_sc_tot = Turns(turns_scs * OUT.turns_c)
    OUT.tape_length = Kilometers(OUT.turns_sc_tot * MAGNET.r_centre * 2 * math.pi / 1e3)

    OUT.cost_sc = Currency(max_tape_current / 1e3 * OUT.tape_length * 1e3 * COILS.m_cost_ybco / 1e6)
    OUT.cost_cu = Currency(COILS.frac_cs_cu_yuhu * COILS.m_cost_cu * OUT.vol_coil * COILS.cu_density / 1e6)
    OUT.cost_ss = Currency(COILS.frac_cs_ss_yuhu * COILS.m_cost_ss * OUT.vol_coil * COILS.ss_density / 1e6)
    OUT.tot_mat_cost = Currency(OUT.cost_sc + OUT.cost_cu + OUT.cost_ss)

    OUT.magnet_cost = Currency(OUT.tot_mat_cost * COILS.mfr_factor)
    OUT.magnet_struct_cost = Currency(COILS.struct_factor * OUT.magnet_cost)
    OUT.magnet_total_cost_individual = Currency(OUT.magnet_cost + OUT.magnet_struct_cost)
    OUT.magnet_total_cost = Currency(OUT.magnet_total_cost_individual * MAGNET.coil_count)

    return OUT


def compute_220103_coils(COILS: Coils, OUT: CAS22):
    # Cost Category 22.1.3: Coils
    OUT.magnet_properties = [compute_magnet_properties(COILS, magnet) for magnet in COILS.magnets]

    # Assuming magCosts[0] is for the first type of coils
    OUT.C22010301 = Currency(OUT.magnet_properties[0].magnet_total_cost)

    # Sum of costs for other types of coils
    OUT.C22010302 = Currency(sum([mag.magnet_total_cost for mag in OUT.magnet_properties[1:]]))
    OUT.C22010303 = Currency(0.05 * (OUT.C22010301 + OUT.C22010302))
    OUT.C22010304 = Currency(sum([mag.magnet_struct_cost for mag in OUT.magnet_properties]))
    OUT.C220103 = Currency(OUT.C22010301 + OUT.C22010302 + OUT.C22010303)

    return OUT

