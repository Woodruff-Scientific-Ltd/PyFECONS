from pyfecons.costing.calculations.cas22.cas220600_other_plant_equipment import compute_other_plant_equipment_costs
from pyfecons.data import Data, TemplateProvider


def cas_2206_other_reactor_plant_equipment(data: Data) -> TemplateProvider:
    # Cost Category 22.6 Other Reactor Plant Equipment
    OUT = data.cas2206
    OUT.C220600 = compute_other_plant_equipment_costs(data.power_table.p_net)
    OUT.template_file = 'CAS220600.tex'
    OUT.tex_path = 'Modified/' + OUT.template_file
    OUT.replacements = {
        'C220600': round(OUT.C220600)
    }
    return OUT
