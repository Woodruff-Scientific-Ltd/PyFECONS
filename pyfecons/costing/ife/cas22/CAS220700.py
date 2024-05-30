from pyfecons.costing.calculations.cas22.cas220700_instrumentation_and_control import \
    compute_instrumentation_and_control_costs
from pyfecons.data import Data, TemplateProvider


def cas_2207_instrumentation_and_control(data: Data) -> TemplateProvider:
    # Cost Category 22.7 Instrumentation and Control
    OUT = data.cas2207
    OUT.C220700 = compute_instrumentation_and_control_costs()
    OUT.template_file = 'CAS220700.tex'
    OUT.replacements = {
        'C220700': round(data.cas2207.C220700)
    }
    return OUT
