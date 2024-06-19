from pyfecons.costing.calculations.cas22.cas220101_reactor_equipment import compute_reactor_equipment_costs
from pyfecons.enums import ReactorType
from pyfecons.inputs import Blanket, RadialBuild
from pyfecons.units import M_USD


def compute_cas22_reactor_equipment_total_cost(reactor_type: ReactorType, blanket: Blanket,
                                               radial_build: RadialBuild) -> M_USD:
    result = compute_reactor_equipment_costs(reactor_type, blanket, radial_build)
    return result.C220101
