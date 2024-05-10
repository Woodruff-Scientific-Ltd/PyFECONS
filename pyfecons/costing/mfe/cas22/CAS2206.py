from pyfecons.data import Data, TemplateProvider
from pyfecons.units import M_USD


def cas_2206_other_reactor_plant_equipment(data: Data) -> TemplateProvider:
    # Cost Category 22.6 Other Reactor Plant Equipment
    OUT = data.cas2206
    # from Waganer, L., 2013. ARIES Cost Account Documentation. [pdf] San Diego: University of California, San Diego.
    #   Available at: https://cer.ucsd.edu/_files/publications/UCSD-CER-13-01.pdf
    OUT.C220600 = M_USD(11.5 * (data.power_table.p_net / 1000) ** 0.8)

    OUT.template_file = 'CAS220600.tex'
    OUT.tex_path = 'Modified/' + OUT.template_file
    OUT.replacements = {
        'C220600': str(OUT.C220600)
    }
    return OUT
