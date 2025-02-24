from pyfecons.costing.calculations.cas22.cas220101_reactor_equipment import (
    plot_radial_build,
    compute_220101_replacements,
    compute_reactor_equipment_costs,
)
from pyfecons.data import Data, TemplateProvider
from pyfecons.inputs import Inputs


def cas_220101_reactor_equipment(inputs: Inputs, data: Data) -> TemplateProvider:
    # Cost Category 22.1.1: Reactor Equipment
    IN = inputs.radial_build
    reactor_type = inputs.basic.reactor_type
    confinement_type = inputs.basic.confinement_type
    blanket = inputs.blanket

    OUT = data.cas220101 = compute_reactor_equipment_costs(
        reactor_type, confinement_type, blanket, IN
    )
    OUT.figures["Figures/radial_build.pdf"] = plot_radial_build(reactor_type, IN)

    OUT.template_file = "CAS220101_IFE_DT.tex"
    OUT.replacements = compute_220101_replacements(reactor_type, blanket, IN, OUT)
    return OUT
