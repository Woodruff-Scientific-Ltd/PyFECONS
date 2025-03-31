from dataclasses import dataclass, field

from pyfecons.report import ReportSection
from pyfecons.units import M_USD, Kilograms, USD


@dataclass
class VesselCost:
    name: str = None
    total_mass: Kilograms = 0
    material_cost: USD = 0
    fabrication_cost: USD = 0
    total_cost: USD = 0


@dataclass
class VesselCosts:
    spool_assembly: VesselCost = field(default_factory=VesselCost)
    removable_doors: VesselCost = field(default_factory=VesselCost)
    door_frames: VesselCost = field(default_factory=VesselCost)
    port_enclosures: VesselCost = field(default_factory=VesselCost)
    total: VesselCost = field(default_factory=VesselCost)
    contingency: VesselCost = field(default_factory=VesselCost)
    prime_contractor_fee: VesselCost = field(default_factory=VesselCost)
    total_subsystem_cost: VesselCost = field(default_factory=VesselCost)


@dataclass
class CAS220106(ReportSection):
    # 22.1.6 Vacuum system
    C22010601: M_USD = None
    C22010602: M_USD = None
    C22010603: M_USD = None
    C22010604: M_USD = None
    C220106: M_USD = None
    massstruct: float = None
    vesvol: float = None
    vesmatcost: float = None
    vessel_costs: VesselCosts = field(default_factory=VesselCosts)
