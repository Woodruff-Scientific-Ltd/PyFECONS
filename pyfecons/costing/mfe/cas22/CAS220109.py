import math

from pyfecons.data import Data, TemplateProvider
from pyfecons.inputs import Inputs
from pyfecons.units import M_USD


def cas_220109_direct_energy_converter(inputs: Inputs, data: Data) -> TemplateProvider:
    # 22.1.9 Direct Energy Converter
    IN = inputs.direct_energy_converter
    OUT = data.cas220109

    # Subsystem costs
    # Data scaled from Post, R.F., 1970. Mirror systems: fuel cycles, loss reduction and energy recovery.
    #   In Nuclear fusion reactors (pp. 99-111). Thomas Telford Publishing.
    OUT.costs = {
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

    if inputs.basic.noak:
        OUT.costs["contingency15percent"] = M_USD(0)

    # Scaling with system size
    def scaled_cost(cost: M_USD) -> M_USD:
        return M_USD(cost * IN.system_power * (1 / math.sqrt(IN.flux_limit)) ** 3)

    OUT.scaled_costs = {key: M_USD(scaled_cost(value)) for key, value in OUT.costs.items()}
    # TODO verify this right now the script pulls "totaldecost": 591, which is not the sum of the parts
    # OUT.C220109 = M_USD(sum(OUT.scaled_costs.values()))
    # TODO why is this zero?
    OUT.C220109 = M_USD(0)

    OUT.template_file = 'CAS220109.tex'
    OUT.tex_path = 'Modified/' + OUT.template_file
    OUT.replacements = {key: round(value, 1) for key, value in OUT.scaled_costs.items()}
    OUT.replacements['totaldecost'] = round(M_USD(sum(OUT.scaled_costs.values())), 1)
    OUT.replacements['C220109'] = OUT.C220109
    return OUT
