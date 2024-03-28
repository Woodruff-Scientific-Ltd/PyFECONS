import math
import matplotlib.pyplot as plt
import numpy as np
import cadquery as cq

from pyfecons import BlanketFirstWall, BlanketType
from pyfecons.inputs import (Inputs, Basic, Coils, Magnet, SupplementaryHeating, PrimaryStructure, PowerSupplies,
                             DirectEnergyConverter, Installation, FuelHandling)
from pyfecons.data import Data, CAS22, MagnetProperties, PowerTable
from pyfecons.units import M_USD, Kilometers, Turns, Amperes, Meters2, MA, Meters3, Meters, Kilograms

CAS_220101_MFE_DT_TEX = 'CAS220101_MFE_DT.tex'


def GenerateData(inputs: Inputs, data: Data, figures: dict):
    OUT = data.cas22
    compute_220101_reactor_equipment(inputs, data, figures)
    compute_220102_shield(inputs, data, figures)
    compute_220103_coils(inputs.coils, OUT)
    compute_220104_supplementary_heating(inputs.supplementary_heating, OUT)
    compute_220105_primary_structure(inputs.primary_structure, data.power_table, OUT)
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

    # Volumes for torus
    def calc_volume_torus(inner, outer):
        return np.pi * IN.axis_t * (inner + outer) ** 2  # V_tok_b	= pi*L*(a_tok + d)^2 - V_tok_p;

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
    # TODO - what are these constants: 9, 0.779, 40?
    OUT.coil_vol = Meters3(calc_volume_torus(OUT.coil_ir, IN.coil_t) * (9 * 0.779) / 40)

    # Volumes for sphere
    def calc_volume_sphere(inner, outer):
        return 4 / 3 * np.pi * (outer ** 3 - inner ** 3)

    # TODO - debug why these are returning negative volumes
    OUT.gap2_vol = calc_volume_sphere(OUT.gap2_ir, IN.gap2_t)  # must be cylindrical in all cases
    OUT.bioshield_vol = calc_volume_sphere(OUT.bioshield_ir, IN.bioshield_t)  # Updated bioshield volume

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
        OUT.C22010102 = M_USD(OUT.blanket1_vol * materials.Li4SiO4.rho * materials.Li4SiO4.c_raw * materials.Li4SiO4.m / 1e6)
    elif blanket.blanket_type == BlanketType.SOLID_FIRST_WALL_WITH_A_SOLID_BREEDER_LI2TIO3:
        OUT.C22010102 = M_USD(OUT.blanket1_vol * materials.Li2TiO3.rho * materials.Li2TiO3.c_raw * materials.Li2TiO3.m / 1e6)
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

def compute_220102_shield(inputs: Inputs, data: Data, figures: dict):
    OUT = data.cas22
    cas220101 = data.cas220101
    materials = inputs.materials
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
    OUT.C22010201 = round(C_HTS, 1)
    OUT.C22010202 = cas220101.lt_shield_vol * materials.SS316.c_raw * materials.SS316.m / 1e3
    OUT.C22010203 = cas220101.bioshield_vol * materials.SS316.c_raw * materials.SS316.m / 1e3
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


def compute_220106_vacuum_system(inputs: Inputs, data: Data, figures: dict):
    # 22.1.6 Vacuum system
    OUT = data.cas22
    vacuum_system = inputs.vacuum_system

    # 22.1.6.1 Vacuum Vessel
    # Parameters
    middle_length = data.cas220101.vacuum_ir  # Middle part length in meters
    middle_diameter = 2 * data.cas220101.vessel_ir  # Middle part diameter in meters
    end_length = vacuum_system.end_length  # End parts length in meters (each)
    end_diameter = 3 * data.cas220101.vessel_ir  # End parts diameter in meters
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
        return data.power_table.p_neutron * 0.05 / 1e6

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
    OUT.C220100 = M_USD(data.cas220101.C220101 + OUT.C220102 + OUT.C220103 + OUT.C220104
                        + OUT.C220105 + OUT.C220106 + OUT.C220107 + OUT.C220111)


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
