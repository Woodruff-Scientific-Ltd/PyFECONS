from pyfecons.costing.calculations.cas22.cas22_reactor_plant_equipment_total import compute_cas22_total_costs, \
    compute_replacements
from pyfecons.data import Data, TemplateProvider


def cas_2200_reactor_plant_equipment_total(data: Data) -> TemplateProvider:
    # Reactor Plant Equipment (RPE) total
    OUT = data.cas22
    OUT = compute_cas22_total_costs(OUT, data)
    OUT.template_file = 'CAS220000.tex'
    OUT.replacements = compute_replacements(data)
    return OUT
