import numpy as np

from pyfecons.costing.calculations.conversions import inflation_2005_2024, to_m_usd
from pyfecons.costing.calculations.thermal import (
    k_steel,
    compute_q_in_struct,
    compute_q_in_n,
    compute_iter_cost_per_MW,
)
from pyfecons.data import Data, TemplateProvider, VesselCosts, VesselCost
from pyfecons.inputs import Inputs
from pyfecons.units import Kilograms, USD, M_USD


def cas_220106_vacuum_system(inputs: Inputs, data: Data) -> TemplateProvider:
    # 22.1.6 Vacuum system
    OUT = data.cas220106
    IN = inputs.vacuum_system
    build = data.cas220101

    # 22.1.6.1 Vacuum Vessel
    # from radial build
    syst_spool_ir = (
        build.axis_ir - (build.vessel_ir - build.axis_ir) * 0.5
    )  # Spool inner radius (goes around CS)
    syst_doors_ir = build.vessel_ir  # doors inner radius (goes within TF)
    syst_height = (
        inputs.radial_build.elon * build.vessel_vol / (np.pi * build.vessel_ir**2)
    )  # System height

    # Cost reference from: Lester M. Waganer et al., 2006, Fusion Engineering and Design. URL:
    #   http://qedfusion.org/LIB/REPORT/CONF/ACTsyscodedocs/ASC_FED2_Dragojlovic.pdf
    # TODO figure out why intellij is giving warnings for these assignments
    OUT.vessel_costs = VesselCosts(
        spool_assembly=VesselCost(
            name="Spool assembly",
            total_mass=Kilograms(136043),
            material_cost=USD(49430),
            fabrication_cost=USD(2614897),
            total_cost=USD(2800370),
        ),
        removable_doors=VesselCost(
            name="Removable doors",
            total_mass=Kilograms(211328),
            material_cost=USD(859863),
            fabrication_cost=USD(6241880),
            total_cost=USD(7313071),
        ),
        door_frames=VesselCost(
            name="Doorframes",
            total_mass=Kilograms(53632),
            material_cost=USD(356555),
            fabrication_cost=USD(2736320),
            total_cost=USD(3146507),
        ),
        port_enclosures=VesselCost(
            name="Port enclosures",
            total_mass=Kilograms(712448),
            material_cost=USD(2020698),
            fabrication_cost=USD(14309096),
            total_cost=USD(17042242),
        ),
        total=VesselCost(name="Total"),
        contingency=VesselCost(name="Contingency (20%)"),
        prime_contractor_fee=VesselCost(name="Prime contractor fee (12%)"),
        total_subsystem_cost=VesselCost(name="Total subsystem cost"),
    )

    for cost in [
        OUT.vessel_costs.spool_assembly,
        OUT.vessel_costs.removable_doors,
        OUT.vessel_costs.door_frames,
        OUT.vessel_costs.port_enclosures,
    ]:
        geometry_factor = (
            (syst_spool_ir / IN.spool_ir) * (syst_height / IN.spool_height)
            if cost.name == "Spool assembly"
            else (syst_doors_ir / IN.door_irb) * (syst_height / IN.spool_height)
        )
        cost.total_mass = cost.total_mass * geometry_factor

        # Scaling costs based on new mass
        if cost.total_mass > 0:
            # New cost based on per kg rate, applying learning credit and inflation
            cost.material_cost = (
                cost.material_cost
                * geometry_factor
                * IN.learning_credit
                * inflation_2005_2024
            )
            cost.fabrication_cost = (
                cost.fabrication_cost
                * geometry_factor
                * IN.learning_credit
                * inflation_2005_2024
            )

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
    OUT.vessel_costs.total_subsystem_cost.total_cost = (
        total_cost
        + OUT.vessel_costs.contingency.total_cost
        + OUT.vessel_costs.prime_contractor_fee.total_cost
    )

    # Calculate mass and cost
    OUT.massstruct = OUT.vessel_costs.total.total_mass
    OUT.vesvol = np.pi * (syst_doors_ir**2 - syst_spool_ir**2) * syst_height
    OUT.C22010601 = to_m_usd(OUT.vessel_costs.total_subsystem_cost.total_cost)

    # COOLING 22.1.3.2
    # INPUTS
    T_op = 20  # Operating temerature of magnets
    T_env = 300  # Temperature of environment (to be cooled from)

    def calc_torus_sa(min_r: float, maj_r: float):
        return 4 * np.pi**2 * maj_r * min_r

    # Scaling cooling costs from ITER see Serio, L., ITER Organization and Domestic Agencies and Collaborators,
    #  2010, April. Challenges for cryogenics at ITER. In AIP Conference Proceedings (Vol. 1218, No. 1, pp. 651-662).
    #  American Institute of Physics.
    coils = inputs.coils
    load_area_1 = calc_torus_sa((build.ht_shield_ir - build.axis_ir), build.axis_ir)
    load_area_2 = calc_torus_sa((build.lt_shield_ir - build.axis_ir), build.axis_ir)
    p_neutron = data.power_table.p_neutron
    # Neutron heat load on HT Shield
    q_in_n = compute_q_in_n(
        load_area_1, p_neutron, build.coil_ir, build.axis_ir
    ) + 0.1 * compute_q_in_n(load_area_2, p_neutron, build.coil_ir, build.axis_ir)
    q_in_struct = compute_q_in_struct(
        coils, k_steel((coils.t_env + coils.t_op) / 2), (coils.t_env + coils.t_op) / 2
    )
    q_in = q_in_struct + q_in_n  # total input heat for one coil

    OUT.C22010602 = M_USD(q_in * compute_iter_cost_per_MW(coils))

    # VACUUM PUMPING 22.1.6.3
    # Number of vacuum pumps required to pump the full vacuum in 1 second
    no_vpumps = int(OUT.vesvol / IN.vpump_cap)
    OUT.C22010603 = to_m_usd(no_vpumps * IN.cost_pump)

    # ROUGHING PUMP 22.1.6.4
    # from STARFIRE, only 1 needed
    # TODO where do these constants come from?
    OUT.C22010604 = to_m_usd(120000 * 2.85)

    OUT.C220106 = M_USD(OUT.C22010601 + OUT.C22010602 + OUT.C22010603 + OUT.C22010604)
    OUT.template_file = "CAS220106_MFE.tex"
    OUT.replacements = {
        "C22010601": round(OUT.C22010601),
        "C22010602": round(OUT.C22010601),
        "C22010603": round(OUT.C22010603),
        "C22010604": round(OUT.C22010604),
        "C22010600": round(OUT.C220106),
        "vesvol": round(OUT.vesvol),
        "massstruct": round(OUT.massstruct),
        "vesmatcost": round(to_m_usd(OUT.vessel_costs.total.material_cost), 1),
    }
    return OUT
