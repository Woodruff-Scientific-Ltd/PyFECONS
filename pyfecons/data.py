from pyfecons.enums import *
from pyfecons.inputs import *
from pyfecons.serializable import SerializableToJSON

class Data(SerializableToJSON):
    class PowerTable:
        def __init__(self):
            self.p_alpha: MW
            self.p_neutron: MW
            self.p_cool : MW
            self.p_aux : MW
            self.p_coils : MW

            self.p_th : MW
            self.p_the : MW
            self.p_dee : MW

            self.p_et : MW
            self.p_loss : MW
            self.p_pump : MW
            self.p_sub : MW
            self.qsci : Unknown
            self.qeng : Unknown
            self.refrac : Unknown
            self.p_net : MW
    class CAS10:
        def __init__(self):
            self.C110000: Currency
            self.C120000: Currency
            self.C130000: Currency
            self.C140000: Currency
            self.C150000: Currency
            self.C160000: Currency
            self.C170000: Currency
            self.C190000: Currency
            self.C100000: Currency
    class CAS21:
        def __init__(self):
            self.C210100: Currency
            self.C210200: Currency
            self.C210300: Currency
            self.C210400: Currency
            self.C210500: Currency
            self.C210600: Currency
            self.C210700: Currency
            self.C210800: Currency
            self.C210900: Currency
            self.C211000: Currency
            self.C211100: Currency
            self.C211200: Currency
            self.C211300: Currency
            self.C211400: Currency
            self.C211500: Currency
            self.C211600: Currency
            self.C211700: Currency
            self.C211800: Currency
            self.C210000: Currency

    class CAS22:
        def __init__(self):
            # Inner radii
            self.axis_ir: Meters
            self.plasma_ir: Meters
            self.vacuum_ir: Meters
            self.firstwall_ir: Meters
            self.blanket1_ir: Meters
            self.reflector_ir: Meters
            self.ht_shield_ir: Meters
            self.structure_ir: Meters
            self.gap1_ir: Meters
            self.vessel_ir: Meters
            self.lt_shield_ir: Meters  # Moved lt_shield here
            self.coil_ir: Meters  # Updated coil_ir calculation
            self.gap2_ir: Meters
            self.bioshield_ir: Meters  # Updated bioshield inner radius

            # Outer radii
            self.axis_or: Meters
            self.plasma_or: Meters
            self.vacuum_or: Meters
            self.firstwall_or: Meters
            self.blanket1_or: Meters
            self.reflector_or: Meters
            self.ht_shield_or: Meters
            self.structure_or: Meters
            self.gap1_or: Meters
            self.vessel_or: Meters
            self.lt_shield_or: Meters  # Moved lt_shield here
            self.coil_or: Meters  # Updated coil_or calculation
            self.gap2_or: Meters
            self.bioshield_or: Meters  # Updated bioshield outer radius

            # Volumes for cylinder
            self.axis_vol: Meters3
            self.plasma_vol: Meters3
            self.plasma_vol: Meters3
            self.vacuum_vol: Meters3
            self.firstwall_vol: Meters3
            self.blanket1_vol: Meters3
            self.reflector_vol: Meters3
            self.ht_shield_vol: Meters3
            self.structure_vol: Meters3
            self.gap1_vol: Meters3
            self.vessel_vol: Meters3
            self.lt_shield_vol: Meters3  # Moved lt_shield volume here
            self.coil_vol: Meters3  # Updated coil volume calculation
            self.gap2_vol: Meters3
            self.bioshield_vol: Meters3  # Updated bioshield volume

    def __init__(self):
        self.power_table = Data.PowerTable()
        self.cas10 = Data.CAS10()
        self.cas21 = Data.CAS21()
        self.cas22 = Data.CAS22()