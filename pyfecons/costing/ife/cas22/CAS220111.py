from pyfecons.costing.calculations.cas22.cas220111_installation_costs import compute_installation_costs
from pyfecons.data import Data, TemplateProvider
from pyfecons.inputs import Inputs


def cas_220111_installation_costs(inputs: Inputs, data: Data) -> TemplateProvider:
    # Cost Category 22.1.11 Installation costs
    IN = inputs.installation
    basic = inputs.basic
    OUT = data.cas220111

    OUT.C220111 = compute_installation_costs(IN.labor_rate, basic.construction_time, basic.n_mod, data.cas220101.axis_ir)
    OUT.template_file = 'CAS220111.tex'
    OUT.tex_path = 'Modified/' + OUT.template_file
    OUT.replacements = {
        'C220111': str(OUT.C220111),
        'constructionTime': round(basic.construction_time),
        'billingRate': round(IN.labor_rate)
    }
    return OUT
