from pyfecons.costing.accounting.power_table import PowerTable
from pyfecons.costing.categories.cas220108_target_factory import CAS220108TargetFactory
from pyfecons.costing.models.target_factory_cost import CostField, TargetFactoryCost
from pyfecons.inputs.target_factory import TargetFactory
from pyfecons.units import M_USD


def cas_220108_target_factory_costs(
    target_factory: TargetFactory, power_table: PowerTable
) -> CAS220108TargetFactory:
    # 22.1.8 Target factory
    cas220108: CAS220108TargetFactory = CAS220108TargetFactory()
    p_net = power_table.p_net

    # TODO these are not used, therefore commented out
    # released per target from https://www.sciencedirect.com/science/article/abs/pii/S0920379613007357
    # life_target_yield = MJ(132)
    # required PRF to acheive target PNRL (assuming exact target design as specified)
    # syst_prf = inputs.basic.p_nrl / life_target_yield

    cas220108.target_factory_costs = {
        "CVD diamond ablator": TargetFactoryCost(
            no_machines=CostField(250),
            floorspace_sqrft=CostField(40315),
            wip_parts=CostField(26769613),
            tcc_dollars=CostField(72627250),
            annualized_cc_dollars_per_year=CostField(5586712),
            consumables_electricity_maint=CostField(33617103),
            personnel_costs_dollars_per_year=CostField(6250000),
            cost_per_target=CostField(0.096),
        ),
        "DT Fill": TargetFactoryCost(
            no_machines=CostField(57),
            floorspace_sqrft=CostField(1858),
            wip_parts=CostField(52),
            tcc_dollars=CostField(70553750),
            annualized_cc_dollars_per_year=CostField(5427212),
            consumables_electricity_maint=CostField(4120108),
            personnel_costs_dollars_per_year=CostField(1425000),
            cost_per_target=CostField(0.023),
        ),
        "Hohlraum press": TargetFactoryCost(
            no_machines=CostField(4),
            floorspace_sqrft=CostField(680),
            wip_parts=CostField(4),
            tcc_dollars=CostField(3759140),
            annualized_cc_dollars_per_year=CostField(289165),
            consumables_electricity_maint=CostField(758791),
            personnel_costs_dollars_per_year=CostField(100000),
            cost_per_target=CostField(0.011),
        ),
        "Tent assy": TargetFactoryCost(
            no_machines=CostField(15),
            floorspace_sqrft=CostField(568),
            wip_parts=CostField(6448),
            tcc_dollars=CostField(1694905),
            annualized_cc_dollars_per_year=CostField(130377),
            consumables_electricity_maint=CostField(548766),
            personnel_costs_dollars_per_year=CostField(375000),
            cost_per_target=CostField(0.005),
        ),
        "Hohlraum-capsule assy": TargetFactoryCost(
            no_machines=CostField(84),
            floorspace_sqrft=CostField(2016),
            wip_parts=CostField(78),
            tcc_dollars=CostField(2185376),
            annualized_cc_dollars_per_year=CostField(168106),
            consumables_electricity_maint=CostField(2542416),
            personnel_costs_dollars_per_year=CostField(2100000),
            cost_per_target=CostField(0.012),
        ),
        "LEH window attach": TargetFactoryCost(
            no_machines=CostField(91),
            floorspace_sqrft=CostField(2919),
            wip_parts=CostField(91),
            tcc_dollars=CostField(90828500),
            annualized_cc_dollars_per_year=CostField(6986808),
            consumables_electricity_maint=CostField(3124288),
            personnel_costs_dollars_per_year=CostField(2275000),
            cost_per_target=CostField(0.025),
        ),
        "DT ice form": TargetFactoryCost(
            no_machines=CostField(1),
            floorspace_sqrft=CostField(27),
            wip_parts=CostField(561600),
            tcc_dollars=CostField(2257455),
            annualized_cc_dollars_per_year=CostField(173650),
            consumables_electricity_maint=CostField(379143),
            personnel_costs_dollars_per_year=CostField(25000),
            cost_per_target=CostField(0.001),
        ),
        "Recover and recycle": TargetFactoryCost(
            no_machines=CostField(None),
            floorspace_sqrft=CostField(None),
            wip_parts=CostField(None),
            tcc_dollars=CostField(None),
            annualized_cc_dollars_per_year=CostField(None),
            consumables_electricity_maint=CostField(None),
            personnel_costs_dollars_per_year=CostField(None),
            cost_per_target=CostField(0),
        ),
        "Facility management costs": TargetFactoryCost(
            no_machines=CostField(None),
            floorspace_sqrft=CostField(2000),
            wip_parts=CostField(None),
            tcc_dollars=CostField(500000),
            annualized_cc_dollars_per_year=CostField(38462),
            consumables_electricity_maint=CostField(70420),
            personnel_costs_dollars_per_year=CostField(6250000),
            cost_per_target=CostField(0.016),
        ),
        "Add material": TargetFactoryCost(
            no_machines=CostField(None),
            floorspace_sqrft=CostField(None),
            wip_parts=CostField(None),
            tcc_dollars=CostField(None),
            annualized_cc_dollars_per_year=CostField(None),
            consumables_electricity_maint=CostField(None),
            personnel_costs_dollars_per_year=CostField(None),
            cost_per_target=CostField(0.03213),
        ),
        "Total process": TargetFactoryCost(
            no_machines=CostField(502),
            floorspace_sqrft=CostField(50383),
            wip_parts=CostField(27337886),
            tcc_dollars=CostField(244406376),
            annualized_cc_dollars_per_year=CostField(18762029),
            consumables_electricity_maint=CostField(45161035),
            personnel_costs_dollars_per_year=CostField(18800000),
            cost_per_target=CostField(0.189),
        ),
    }

    for cost in cas220108.target_factory_costs.values():
        cost.no_machines.scaling_factor = p_net / 1000
        cost.floorspace_sqrft.scaling_factor = p_net / 1000
        cost.wip_parts.scaling_factor = p_net / 1000 * 1e-6
        cost.tcc_dollars.scaling_factor = p_net / 1000 * 1e-6
        cost.annualized_cc_dollars_per_year.scaling_factor = p_net / 1000 * 1e-6
        cost.consumables_electricity_maint.scaling_factor = p_net / 1000 * 1e-6
        cost.personnel_costs_dollars_per_year.scaling_factor = p_net / 1000 * 1e-6
        cost.cost_per_target.scaling_factor = (
            p_net / 1000 * target_factory.learning_credit
        )

    # TODO these are not used so skipping calculation
    # total_annualized_cc = sum([cost.annualized_cc_dollars_per_year.scaled_cost for cost in target_factory_costs.values()])
    # total_consumables_electricity_maint = sum([cost.consumables_electricity_maint.scaled_cost for cost in target_factory_costs.values()])
    # total_personnel_costs = sum([cost.personnel_costs_dollars_per_year.scaled_cost for cost in target_factory_costs.values()])
    # total_target_costs = sum([cost.cost_per_target.scaled_cost for cost in target_factory_costs.values()])

    # TODO this is not used
    # tot_targets = inputs.basic.implosion_frequency * 3.154e7

    # TODO this is a very very small number, is the scaling correct?
    cas220108.C220108 = M_USD(
        cas220108.target_factory_costs["Total process"].tcc_dollars.scaled_cost / 1e6
    )
    return cas220108
