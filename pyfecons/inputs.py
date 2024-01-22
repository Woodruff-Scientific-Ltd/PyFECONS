from pyfecons.enums import *
from pyfecons.units import *
from pyfecons.materials import Materials
from pyfecons.serializable import SerializableToJSON

# This class will contain every possible input
# It will not contain information about which inputs will actually used by the costing code and which ones won't
# The DefineInputs.py script in each customer folder is in charge of making sure all of the appropriate inputs are set
# The costing code itself should throw appropriate errors when necessary inputs are not set
# The logical flow of inputs & inputs dependencies will be documented here
# https://docs.google.com/spreadsheets/d/115j-R-XZX9JI_VGt4AR7T3fZ91Qdmtc-WfEg_CpSlKE/edit?usp=sharing
# The units, descriptions, and expected values will also be documented on the spreadsheet

# The classes within Inputs must maintain their own toDict function
# In addition, the Inputs class itself maintains its own toDict function that calls upon the sublcasses
class Inputs (SerializableToJSON):
    class CustomerInfo:
        def __init__(self, name: str = ''):
            self.name = name

    class Basic:
        def __init__(self,
                reactor_type: ReactorType = ReactorType.IFE,
                energy_conversion: EnergyConversion = EnergyConversion.DIRECT,
                fuel_type: FuelType = FuelType.DT,
                p_nrl: MW = 2600.0,
                n_mod: Count = 1,
                am: Percent = 1.00,
                construction_time: Years = 6.0,
                plant_lifetime: Years = 30.0,
                plant_availability: Percent = 0.85,
                ):
            self.reactor_type = reactor_type
            self.energy_conversion = energy_conversion
            self.fuel_type = fuel_type
            self.p_nrl = p_nrl
            self.n_mod = n_mod
            self.am = am
            self.constructionTime = construction_time
            self.plant_lifetime = plant_lifetime
            self.plant_availability = plant_availability

    class PowerTable:
        def __init__(self):
            self.f_sub: Percent = 0.03
            self.p_cryo: MW = 0.5
            self.mn : Ratio = 1.1
            self.eta_p : Percent = 0.5
            self.eta_th : Percent = 0.46
            self.fpcppf : Percent = 0.06
            self.p_trit : MW = 10
            self.p_house : MW = 4
            self.p_tfcool : MW = 12.7
            self.p_pfcool : MW = 1
            self.p_tf : MW = 1
            self.p_pf : MW = 1
            self.eta_pin : Percent = 0.5
            self.eta_pin1 : Percent = 0.18
            self.eta_pin2 : Percent = 0.82
            self.eta_de : Percent = 0.85
            self.p_input : MW = 50

    class RadialBuild:
        def __init__(self):
            self.chamber_length: Meters = 40#[m] chamber length
            self.axis_t: Meters = 0#[m] central axis thickness
            self.plasma_t: Meters = 4#[m] Radial plasma thickness
            self.vacuum_t: Meters = 0.1 #[m] Radial vacuum thickness
            self.firstwall_t: Meters = 0.1#[m] Radial firstwall thickness
            self.blanket1_t: Meters = 1 #[m] Radial blanket thickness
            self.reflector_t: Meters = 0.1 #[m] Radial reflector thickness
            self.ht_shield_t: Meters = 0.5 #[m] Radial high temperature shield thickness
            self.structure_t: Meters = 0.2 #[m] Radial structure thickness
            self.gap1_t: Meters = 0.5 #[m] Radial first gap thickness
            self.vessel_t: Meters = 0.2 #[m] Radial vessel wall thickness
            self.coil_t: Meters = 1.76 #[m] Radial coil thickness
            self.gap2_t: Meters = 1 #[m] Radial second gap thickness
            self.lt_shield_t: Meters = 0.3 #[m] Radial low temperature shield thickness
            self.bioshield_t: Meters = 1 #[m] Radial bioshield thickness

    def __init__(self,
                 customer_info: CustomerInfo = CustomerInfo(),
                 basic: Basic = Basic(),
                 power_table: PowerTable = PowerTable(),
                 radial_build: RadialBuild = RadialBuild()
                 ):
        
        # User inputs
        self.customer_info = customer_info
        self.basic = basic
        self.power_table = power_table
        self.radial_build = radial_build

        # Library inputs
        self.materials: Materials = Materials()
