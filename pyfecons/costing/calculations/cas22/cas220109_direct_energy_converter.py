import math

from pyfecons.data import CAS220109, Data
from pyfecons.inputs.all_inputs import AllInputs
from pyfecons.inputs.direct_energy_converter import DirectEnergyConverter
from pyfecons.report import TemplateProvider
from pyfecons.units import M_USD


def cas_220109_direct_energy_converter_costs(
    inputs: AllInputs, data: Data
) -> TemplateProvider:
    # 22.1.9 Direct Energy Converter
    IN = inputs.direct_energy_converter
    OUT = data.cas220109

    OUT.costs = get_subsystem_costs(inputs.basic.noak)
    OUT.scaled_costs = get_scaled_costs(OUT.costs, IN)

    # TODO verify this right now the script pulls "totaldecost": 591, which is not the sum of the parts
    # OUT.C220109 = M_USD(sum(OUT.scaled_costs.values()))
    # TODO why is this zero?
    OUT.C220109 = M_USD(0)

    OUT.template_file = "CAS220109.tex"
    OUT.replacements = get_replacements(OUT)
    return OUT


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


def get_replacements(OUT: CAS220109) -> dict[str, str]:
    replacements = {
        key: str(round(value, 1)) for key, value in OUT.scaled_costs.items()
    }
    replacements["totaldecost"] = str(round(sum(OUT.scaled_costs.values()), 1))
    replacements["C220109"] = str(OUT.C220109)
    return replacements
