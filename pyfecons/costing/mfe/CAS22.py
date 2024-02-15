import math
import matplotlib.pyplot as plt
import numpy as np
import cadquery as cq

from pyfecons.inputs import Inputs, Basic, RadialBuild, Coils, Magnet, SupplementaryHeating, PrimaryStructure, \
    VacuumSystem, PowerSupplies
from pyfecons.data import Data, CAS22, MagnetProperties, PowerTable
from pyfecons.materials import Materials
from pyfecons.units import M_USD, Kilometers, Turns, Amperes, Meters2, MA, Meters3, Meters, Kilograms


def GenerateData(inputs: Inputs, data: Data, figures: dict):
    OUT = data.cas22
    compute_220101_reactor_equipment(inputs.basic, inputs.radial_build, inputs.materials, OUT)
    compute_220102_shield(inputs.materials, OUT)
    compute_220103_coils(inputs.coils, OUT)
    compute_220104_supplementary_heating(inputs.supplementary_heating, OUT)
    compute_220105_primary_structure(inputs.primary_structure, data.power_table, OUT)
    compute_220106_vacuum_system(inputs.vacuum_system, data.power_table, OUT)
    compute_220107_power_supplies(inputs.basic, inputs.power_supplies, OUT)
    compute_220108_divertor(inputs.materials, OUT)

    OUT.C220000 = OUT.C220101 + OUT.C220102 + OUT.C220103 + OUT.C220104


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

    OUT.cost_sc = M_USD(max_tape_current / 1e3 * OUT.tape_length * 1e3 * COILS.m_cost_ybco / 1e6)
    OUT.cost_cu = M_USD(COILS.frac_cs_cu_yuhu * COILS.m_cost_cu * OUT.vol_coil * COILS.cu_density / 1e6)
    OUT.cost_ss = M_USD(COILS.frac_cs_ss_yuhu * COILS.m_cost_ss * OUT.vol_coil * COILS.ss_density / 1e6)
    OUT.tot_mat_cost = M_USD(OUT.cost_sc + OUT.cost_cu + OUT.cost_ss)

    OUT.magnet_cost = M_USD(OUT.tot_mat_cost * COILS.mfr_factor)
    OUT.magnet_struct_cost = M_USD(COILS.struct_factor * OUT.magnet_cost)
    OUT.magnet_total_cost_individual = M_USD(OUT.magnet_cost + OUT.magnet_struct_cost)
    OUT.magnet_total_cost = M_USD(OUT.magnet_total_cost_individual * MAGNET.coil_count)

    return OUT


def compute_220103_coils(COILS: Coils, OUT: CAS22):
    # Cost Category 22.1.3: Coils
    OUT.magnet_properties = [compute_magnet_properties(COILS, magnet) for magnet in COILS.magnets]

    # Assuming magCosts[0] is for the first type of coils
    OUT.C22010301 = M_USD(OUT.magnet_properties[0].magnet_total_cost)

    # Sum of costs for other types of coils
    OUT.C22010302 = M_USD(sum([mag.magnet_total_cost for mag in OUT.magnet_properties[1:]]))
    OUT.C22010303 = M_USD(0.05 * (OUT.C22010301 + OUT.C22010302))
    OUT.C22010304 = M_USD(sum([mag.magnet_struct_cost for mag in OUT.magnet_properties]))
    OUT.C220103 = M_USD(OUT.C22010301 + OUT.C22010302 + OUT.C22010303)

    return OUT


def compute_220104_supplementary_heating(supplementary_heating: SupplementaryHeating, OUT: CAS22):
    OUT.C22010401 = supplementary_heating.average_nbi.cost_2023 * supplementary_heating.nbi_power
    OUT.C22010402 = supplementary_heating.average_icrf.cost_2023 * supplementary_heating.icrf_power
    OUT.C220104 = OUT.C22010401 + OUT.C22010402
    return OUT


def compute_220105_primary_structure(primary_structure: PrimaryStructure, power_table: PowerTable, OUT: CAS22):
    # lambda function to compute scaled costs in these calculations
    scaled_cost = lambda cost: cost * power_table.p_et / 1000 * primary_structure.learning_credit

    # standard engineering costs
    OUT.C22010501 = M_USD(scaled_cost(primary_structure.analyze_costs)
                          + scaled_cost(primary_structure.unit1_seismic_costs)
                          + scaled_cost(primary_structure.reg_rev_costs))

    # standard fabrication costs
    OUT.C22010502 = M_USD(
        scaled_cost(primary_structure.unit1_fab_costs) + scaled_cost(primary_structure.unit10_fabcosts))

    # add system PGA costs
    pga_costs = primary_structure.get_pga_costs()
    OUT.C22010501 = M_USD(OUT.C22010501 + pga_costs.eng_costs)
    OUT.C22010502 = M_USD(OUT.C22010502 + pga_costs.fab_costs)

    # total cost calculation
    OUT.C220105 = M_USD(OUT.C22010501 + OUT.C22010502)
    return OUT


def compute_220106_vacuum_system(vacuum_system: VacuumSystem, power_table: PowerTable, OUT: CAS22):
    # 22.1.6 Vacuum system

    # 22.1.6.1 Vacuum Vessel
    # Parameters
    middle_length = OUT.vacuum_ir  # Middle part length in meters
    middle_diameter = 2 * OUT.vessel_ir  # Middle part diameter in meters
    end_length = vacuum_system.end_length  # End parts length in meters (each)
    end_diameter = 3 * OUT.vessel_ir  # End parts diameter in meters
    fillet_radius = 0.022 * middle_length  # Fillet radius in meters, adjust as necessary
    thickness = vacuum_system.thickness  # Thickness in meters

    # Create the middle cylinder
    middle_cylinder = cq.Workplane("XY").cylinder(middle_length, middle_diameter / 2)

    # Create the end cylinders and translate them into position
    end_cylinder1 = cq.Workplane("XY").cylinder(end_length, end_diameter / 2).translate(
        (0, 0, middle_length / 2 + end_length / 2))
    end_cylinder2 = cq.Workplane("XY").cylinder(end_length, end_diameter / 2).translate(
        (0, 0, -(middle_length / 2 + end_length / 2)))

    # Combine the middle cylinder with the end cylinders for outer shape
    combined_outer_shape = middle_cylinder.union(end_cylinder1).union(end_cylinder2)

    # Create an inner middle cylinder with a smaller diameter to represent the thickness
    inner_middle_cylinder = cq.Workplane("XY").cylinder(middle_length, middle_diameter / 2 - thickness)

    # Create inner end cylinders with the reduced diameter and translate them into position
    inner_end_cylinder1 = cq.Workplane("XY").cylinder(end_length, end_diameter / 2 - thickness).translate(
        (0, 0, middle_length / 2 + end_length / 2))
    inner_end_cylinder2 = cq.Workplane("XY").cylinder(end_length, end_diameter / 2 - thickness).translate(
        (0, 0, -(middle_length / 2 + end_length / 2)))

    # Combine the inner middle cylinder with the inner end cylinders for inner shape
    combined_inner_shape = inner_middle_cylinder.union(inner_end_cylinder1).union(inner_end_cylinder2)
    OUT.vesvol = combined_inner_shape.val().Volume()

    # Subtract the combined inner shape from the outer shape for material volume calculation
    material_shape = combined_outer_shape.cut(combined_inner_shape)

    # Calculate the material volume
    OUT.materialvolume = material_shape.val().Volume()

    # Now apply the fillets to the outer shape (for display purposes)
    final_shape_with_fillets = combined_outer_shape.edges().fillet(fillet_radius)

    # Material properties (density and cost)
    ss_density = vacuum_system.ss_density  # kg/m^3
    ss_cost = vacuum_system.ss_cost  # $/kg

    # Calculate mass and cost
    vesmfr = 10
    OUT.massstruct = OUT.materialvolume * ss_density
    OUT.vesmatcost = ss_cost * OUT.massstruct
    OUT.C22010601 = OUT.vesmatcost * vesmfr / 1e6

    # Display the final shape
    # display(final_shape_with_fillets)

    # COOLING 22.1.6.2
    def k_steel(T):
        return vacuum_system.k_steel

    t_mag = vacuum_system.t_mag
    t_env = vacuum_system.t_env

    # Power in from thermal conduction through support
    def qin_struct(no_beams, beam_cs_area, beam_length, k):
        return k * beam_cs_area * no_beams / beam_length * (t_env - t_mag) / 1e6

    # power in from neutron flux, assume 95% is abosrbed in the blanket
    def qin_n():
        return power_table.p_neutron * 0.05 / 1e6

    # cooling from power in/half carnot COP
    c_frac = vacuum_system.c_frac

    def q_cooling(Qin, C_frac):
        COP = t_mag / (t_env - t_mag) * C_frac  # Assume 10% of carnot efficiency
        return Qin / COP, COP

    # For 1 coil, assume 20 support beams, 5m length, 0.5m^2 cs area, target temp of 20K, env temp of 300 K
    OUT.q_in = qin_struct(20, 1, 5, k_steel((t_env + t_mag) / 2)) + qin_n()

    def qin_tot(qin, no_coils):
        return qin * no_coils

    # Cooling power requirements for various temperature differences
    # Generate a range of target temperatures from 20 K to 300 K
    t_mag_range = np.linspace(4, 200, 100)  # Target temperatures

    # Calculating cooling power requirement for different target temperatures
    cooling_power_requirements = qin_tot(OUT.q_in, 13) / (t_mag_range / (t_env - t_mag_range) * c_frac)

    # TODO - finish figure
    # fig, ax = plt.subplots(figsize=(10, 6))
    #
    # # Plotting on the axes
    # ax.plot(t_mag_range, cooling_power_requirements)
    # ax.set_xlabel('Target Temperature (K)')
    # ax.set_ylabel('Cooling Power Requirement (MW)')
    # # ax.set_title('Cooling Power Requirement vs. Target Temperature')
    # ax.grid(True)
    #
    # # Display the plot
    # plt.show()
    #
    # # Export as PDF
    # fig.savefig(os.path.join(figures_directory, 'cooling_efficiency.pdf'), bbox_inches='tight')

    # Scaling cooling costs from STARFIRE see pg40 https://cer.ucsd.edu/_files/publications/UCSD-CER-13-01.pdf
    # Starfire COP
    cop_starfire = 4.2 / (300 - 4.2) * 0.15
    # STARFIRE cooling at 4.2 K
    qsc_itarfire = 20e3  # 20 kW
    # Calculating starfire cooling at system operating temp in MW
    q_cooling_temp = qsc_itarfire * (q_cooling(OUT.q_in, c_frac)[1] / cop_starfire) / 1e6

    # 17.65 M USD in 2009 for 20kW at 4.2 K, adjusted to inflation
    cost_starfire = 17.65 * 1.43
    # M USD, scaled to system size, at system temperature, from the 20 kW cooling, 17.65 STARFIRE system
    OUT.C22010602 = OUT.q_in / q_cooling_temp * 17.65 * 1.43

    # VACUUM PUMPING 22.1.6.3
    # assume 1 second vac rate
    # cost of 1 vacuum pump, scaled from 1985 dollars
    cost_pump = 40000
    # 48 pumps needed for 200^3 system
    # m^3 capable of beign pumped by 1 pump
    vpump_cap = 200 / 48
    # Number of vacuum pumps required to pump the full vacuum in 1 second
    no_vpumps = int(OUT.vesvol / vpump_cap)
    OUT.C22010603 = no_vpumps * cost_pump / 1e6

    # ROUGHING PUMP 22.1.6.4
    # from STARFIRE, only 1 needed
    OUT.C22010604 = 120000 * 2.85 / 1e6

    OUT.C220106 = OUT.C22010601 + OUT.C22010602 + OUT.C22010603 + OUT.C22010604

    return OUT


def compute_220107_power_supplies(basic: Basic, power_supplies: PowerSupplies, OUT: CAS22):
    # Cost Category 22.1.7 Power supplies
    # Scaled relative to ITER for a 500MW fusion power system
    cost_in_kiua = 269.6 * basic.p_nrl / 500 * power_supplies.learning_credit
    OUT.C220107 = M_USD(cost_in_kiua * 2)  # assuming 1kIUA equals $2 M
    return OUT


def compute_220108_divertor(materials: Materials, OUT: CAS22):
    # 22.1.8 Divertor
    # Simple volumetric calculation based on reactor geometry, user input, and tungsten material
    # properties (see "materials" dictionary)
    OUT.divertor_maj_rad = Meters(OUT.coil_ir - OUT.axis_ir)
    OUT.divertor_min_rad = Meters(OUT.firstwall_ir - OUT.axis_ir)
    OUT.divertor_thickness_z = Meters(0.2)
    OUT.divertor_thickness_r = Meters(OUT.divertor_min_rad * 2)
    OUT.divertor_material = materials.W  # Tungsten

    # volume of the divertor based on TF coil radius
    OUT.divertor_vol = Meters3(((OUT.divertor_maj_rad + OUT.divertor_thickness_r) ** 2
                                - (OUT.divertor_maj_rad - OUT.divertor_thickness_r) ** 2)
                               * np.pi * OUT.divertor_thickness_z)
    OUT.divertor_mass = Kilograms(OUT.divertor_vol * OUT.divertor_material.rho)
    OUT.divertor_mat_cost = M_USD(OUT.divertor_mass * OUT.divertor_material.c_raw)
    OUT.divertor_cost = M_USD(OUT.divertor_mat_cost * OUT.divertor_material.m)
    OUT.C220108 = M_USD(OUT.divertor_cost / 1e6)
    return OUT
