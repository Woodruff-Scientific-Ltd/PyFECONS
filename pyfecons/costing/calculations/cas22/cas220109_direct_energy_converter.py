import math

from pyfecons.costing.categories.cas220109 import CAS220109
from pyfecons.inputs.basic import Basic
from pyfecons.inputs.direct_energy_converter import DirectEnergyConverter
from pyfecons.units import M_USD


def cas_220109_direct_energy_converter_costs(
    basic: Basic, direct_energy_converter: DirectEnergyConverter
) -> CAS220109:
    # 22.1.9 Direct Energy Converter
    cas220109 = CAS220109()

    cas220109.costs = get_subsystem_costs(basic.noak)
    cas220109.scaled_costs = get_scaled_costs(cas220109.costs, direct_energy_converter)

    # TODO verify this right now the script pulls "totaldecost": 591, which is not the sum of the parts
    # cas220109.C220109 = M_USD(sum(cas220109.scaled_costs.values()))
    # TODO why is this zero?
    cas220109.C220109 = M_USD(0)
    return cas220109


def get_subsystem_costs(noak: bool) -> dict[str, M_USD]:
    # Subsystem costs
    # Data scaled from Post, R.F., 1970. Mirror systems: fuel cycles, loss reduction and energy recovery.
    #   In Nuclear fusion reactors (pp. 99-111). Thomas Telford Publishing.
    costs = {
        "expandertank": M_USD(16),
        "expandercoilandneutrontrapcoil": M_USD(33),
        "convertoegatevalve": M_USD(0.1),
        "neutrontrapshielding": M_USD(1),
        "vacuumsystem": M_USD(16),
        "gridsystem": M_USD(27),
        "heatcollectionsystem": M_USD(6),
        "electricaleqpmt": M_USD(13),
        "costperunit": M_USD(112),
        "totaldeunitcost": M_USD(447),
        "engineering15percent": M_USD(67),
        "contingency15percent": M_USD(77),
    }
    if noak:
        costs["contingency15percent"] = M_USD(0)
    return costs


def get_scaled_costs(
    costs: dict[str, M_USD], IN: DirectEnergyConverter
) -> dict[str, M_USD]:
    # Scaling with system size
    def scaled_cost(cost: M_USD) -> M_USD:
        return M_USD(cost * IN.system_power * (1 / math.sqrt(IN.flux_limit)) ** 3)

    return {key: scaled_cost(value) for key, value in costs.items()}
