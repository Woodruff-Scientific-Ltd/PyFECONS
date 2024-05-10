from pyfecons.costing.calculations.conversions import inflation_1992_2024
from pyfecons.data import Data, TemplateProvider
from pyfecons.units import M_USD


def cas_2204_radwaste(data: Data) -> TemplateProvider:
    # Cost Category 22.4 Radwaste
    OUT = data.cas2204
    # Radioactive waste treatment
    # base cost of 1.96M from Alexeeva, V., Molloy, B., Beestermoeller, R., Black, G., Bradish, D., Cameron, R.,
    #   Keppler, J.H., Rothwell, G., Urso, M.E., Colakoglu, I. and Emeric, J., 2018. Measuring Employment Generated
    #   by the Nuclear Power Sector (No. NEA--7204). Organisation for Economic Co-Operation and Development.
    OUT.C220400 = M_USD(1.96 * 1e-3 * data.power_table.p_th * inflation_1992_2024)
    OUT.template_file = 'CAS220400.tex'
    OUT.tex_path = 'Modified/' + OUT.template_file
    OUT.replacements = {
        'C220400': str(data.cas2204.C220400)
    }
    return OUT
