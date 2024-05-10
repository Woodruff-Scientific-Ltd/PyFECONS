from pyfecons.data import Data, TemplateProvider
from pyfecons.inputs import Inputs
from pyfecons.units import M_USD


def cas_220111_installation_costs(inputs: Inputs, data: Data) -> TemplateProvider:
    # Cost Category 22.1.11 Installation costs
    IN = inputs.installation
    OUT = data.cas220111

    # Calculations
    # TODO what are 20 and 4? Should they be inputs?
    construction_worker = 20 * data.cas220101.axis_ir / 4
    costs = {
        # TODO what are 20 and 300? Should they be inputs?
        'C_22_1_11_in': IN.nmod * inputs.basic.construction_time * (IN.labor_rate * 20 * 300),
        # TODO for all constants, should they be inputs?
        # TODO why + 0 for all of these
        'C_22_1_11_1_in': IN.nmod * ((IN.labor_rate * 200 * construction_worker) + 0),  # 22.1 first wall blanket
        'C_22_1_11_2_in': IN.nmod * ((IN.labor_rate * 150 * construction_worker) + 0),  # 22.2 shield
        'C_22_1_11_3_in': IN.nmod * ((IN.labor_rate * 100 * construction_worker) + 0),  # coils
        'C_22_1_11_4_in': IN.nmod * ((IN.labor_rate * 30 * construction_worker) + 0),  # supplementary heating
        'C_22_1_11_5_in': IN.nmod * ((IN.labor_rate * 60 * construction_worker) + 0),  # primary structure
        'C_22_1_11_6_in': IN.nmod * ((IN.labor_rate * 200 * construction_worker) + 0),  # vacuum system
        'C_22_1_11_7_in': IN.nmod * ((IN.labor_rate * 400 * construction_worker) + 0),  # power supplies
        'C_22_1_11_8_in': 0,  # guns
        'C_22_1_11_9_in': IN.nmod * ((IN.labor_rate * 200 * construction_worker) + 0),  # direct energy converter
        'C_22_1_11_10_in': 0,  # ECRH
    }

    # Total cost calculations
    OUT.C220111 = M_USD(sum(costs.values()))
    OUT.template_file = 'CAS220111.tex'
    OUT.tex_path = 'Modified/' + OUT.template_file
    OUT.replacements = {
        'C220111': str(OUT.C220111),
        'constructionTime': round(inputs.basic.construction_time),
    }
    return OUT
