from dataclasses import dataclass, field

from pyfecons.inputs.basic import Basic
from pyfecons.inputs.blanket import Blanket
from pyfecons.inputs.coils import Coils
from pyfecons.inputs.customer_info import CustomerInfo
from pyfecons.inputs.direct_energy_converter import DirectEnergyConverter
from pyfecons.inputs.financial import Financial
from pyfecons.inputs.fuel_handling import FuelHandling
from pyfecons.inputs.installation import Installation
from pyfecons.inputs.lasers import Lasers
from pyfecons.inputs.lsa_levels import LsaLevels
from pyfecons.inputs.npv_Input import NpvInput
from pyfecons.inputs.power_supplies import PowerSupplies
from pyfecons.inputs.power_input import PowerInput
from pyfecons.inputs.primary_structure import PrimaryStructure
from pyfecons.inputs.radial_build import RadialBuild
from pyfecons.inputs.shield import Shield
from pyfecons.inputs.supplementary_heating import SupplementaryHeating
from pyfecons.inputs.target_factory import TargetFactory
from pyfecons.inputs.vacuum_system import VacuumSystem
from pyfecons.materials import Materials
from pyfecons.serializable import SerializableToJSON


# This the container class for every possible input and configuration of cost calculations
# The classes within Inputs must maintain their own toDict function
# In addition, the Inputs class itself maintains its own toDict function that calls upon the sublcasses
@dataclass
class AllInputs(SerializableToJSON):
    # User inputs
    customer_info: CustomerInfo = field(default=None)
    basic: Basic = field(default=None)
    power_input: PowerInput = field(default=None)
    radial_build: RadialBuild = field(default=None)
    shield: Shield = field(default=None)
    blanket: Blanket = field(default=None)
    lasers: Lasers = field(default=None)
    coils: Coils = field(default=None)
    # TODO is this really an input? if not move to calculation class
    supplementary_heating: SupplementaryHeating = field(
        default_factory=SupplementaryHeating
    )
    primary_structure: PrimaryStructure = field(default=None)
    vacuum_system: VacuumSystem = field(default=None)
    power_supplies: PowerSupplies = field(default=None)
    direct_energy_converter: DirectEnergyConverter = field(default=None)
    installation: Installation = field(default=None)
    fuel_handling: FuelHandling = field(default=None)
    lsa_levels: LsaLevels = field(default=None)
    # TODO is this really an input? if not move to calculation class
    financial: Financial = field(default_factory=Financial)
    target_factory: TargetFactory = field(default=None)
    npv: NpvInput = field(default=None)

    # created here for reference in inputs.json
    materials: Materials = field(default_factory=Materials)
