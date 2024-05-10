from pyfecons.data import Data, TemplateProvider
from pyfecons.units import M_USD


def cas_220119_scheduled_replacement_cost(data: Data) -> TemplateProvider:
    # Cost category 22.1.19 Scheduled Replacement Cost
    OUT = data.cas220119
    # TODO will this ever be non-zero?
    OUT.C220119 = M_USD(0)
    OUT.template_file = 'CAS220119.tex'
    OUT.tex_path = 'Modified/' + OUT.template_file
    OUT.replacements = {
        'C220119': str(OUT.C220119)
    }
    return OUT
