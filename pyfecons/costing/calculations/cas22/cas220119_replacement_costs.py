from pyfecons.costing.categories.cas220119 import CAS220119
from pyfecons.inputs.primary_structure import PrimaryStructure
from pyfecons.units import M_USD


def cas_220119_scheduled_replacement_costs(
    primary_structure: PrimaryStructure, cas2201_total_cost: M_USD
) -> CAS220119:
    #  Cost category 22.1.19 Scheduled Replacement Cost
    cas220119 = CAS220119()
    cas220119.C220119 = M_USD(cas2201_total_cost * primary_structure.replacement_factor)
    cas220119.template_file = "CAS220119.tex"
    cas220119.replacements = {"C220119": str(round(cas220119.C220119))}
    return cas220119
