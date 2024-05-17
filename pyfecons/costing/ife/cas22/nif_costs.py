from dataclasses import dataclass, field

from pyfecons.inputs import Lasers
from pyfecons.units import M_USD, MW


@dataclass
class NifCost():
    base_key: str
    procurement: M_USD
    design: M_USD
    assembly: M_USD
    total: float = field(init=False)

    def __post_init__(self):
        self.total = self.procurement + self.design + self.assembly

# TODO total cost is fixed for all calculations, is this ok?
# This dictionary contains the NIF 2023 adjusted construction only costs (i.e. excluding pilot+production) for each
NIF_COSTS = {
    '22.1.3. Laser': NifCost(base_key='2213', procurement=M_USD(887.6), design=M_USD(61.2), assembly=M_USD(166.5)),
    '22.1.3.1 Front End': NifCost(base_key='22131FrontEnd', procurement=M_USD(75.0), design=M_USD(9.1), assembly=M_USD(16.0)),
    '22.1.3.2 Main Amp System': NifCost(base_key='22132MainAmpSystem', procurement=M_USD(200.7), design=M_USD(11.1), assembly=M_USD(33.2)),
    '22.1.3.2.1 Main Amp': NifCost(base_key='221321MainAmp', procurement=M_USD(85.3), design=M_USD(5.0), assembly=M_USD(10.2)),
    '22.1.3.2.1.1 Flashlamp Assemblies': NifCost(base_key='2213211FlashlampAssemblies', procurement=M_USD(21.5), design=M_USD(0.0), assembly=M_USD(0.0)),
    '22.1.3.2.1.3, 3.2.1.5-7 (amp mech)': NifCost(base_key='2213213AmpMech', procurement=M_USD(63.9), design=M_USD(5.0), assembly=M_USD(10.2)),
    '22.1.3.2.2 Spatial filters': NifCost(base_key='221322SpatialFilters', procurement=M_USD(27.4), design=M_USD(0.6), assembly=M_USD(6.0)),
    '22.1.3.2.3 Mirror Mounts': NifCost(base_key='221323MirrorMounts', procurement=M_USD(10.0), design=M_USD(0.1), assembly=M_USD(1.0)),
    '22.1.3.2.4 Polarizer assembly': NifCost(base_key='221324PolarizerAssembly', procurement=M_USD(5.2), design=M_USD(0.7), assembly=M_USD(2.7)),
    '22.1.3.2.5 Pockels\' Cell Assembly': NifCost(base_key='221325PockelsCellAssembly', procurement=M_USD(52.6), design=M_USD(4.7), assembly=M_USD(11.1)),
    '22.1.3.2.6 Boost Amp': NifCost(base_key='221326BoostAmp', procurement=M_USD(17.9), design=M_USD(0.0), assembly=M_USD(2.2)),
    '22.1.3.2.6.1 Flashlamp Assemblies': NifCost(base_key='2213261FlashlampAssemblies', procurement=M_USD(4.6), design=M_USD(0.0), assembly=M_USD(0.0)),
    '22.1.3.2.6.3, 3.2.6.5-7 (amp mech)': NifCost(base_key='2213263AmpMech', procurement=M_USD(13.3), design=M_USD(0.0), assembly=M_USD(2.2)),
    '22.1.3.2.7 Interstage Hdw': NifCost(base_key='221327InterstageHdw', procurement=M_USD(2.4), design=M_USD(0.0), assembly=M_USD(0.1)),
    '22.1.3.3 Beam Xport system': NifCost(base_key='22133BeamXportSystem', procurement=M_USD(56.9), design=M_USD(2.8), assembly=M_USD(9.5)),
    '22.1.3.3.1 Spatial filters': NifCost(base_key='221331SpatialFilters', procurement=M_USD(31.1), design=M_USD(2.3), assembly=M_USD(0.0)),
    '22.1.3.3.2 Mirror Assembly': NifCost(base_key='221332MirrorAssembly', procurement=M_USD(8.4), design=M_USD(0.1), assembly=M_USD(7.2)),
    '22.1.3.3.3 Final Optics system': NifCost(base_key='221333FinalOpticsSystem', procurement=M_USD(12.5), design=M_USD(0.3), assembly=M_USD(0.9)),
    '22.1.3.3.4 Beam Tube system': NifCost(base_key='221334BeamTubeSystem', procurement=M_USD(4.9), design=M_USD(0.1), assembly=M_USD(1.3)),
    '22.1.3.3.5 Interstage Hdw': NifCost(base_key='221335InterstageHdw', procurement=M_USD(0.0), design=M_USD(0.0), assembly=M_USD(0.1)),
    '22.1.3.4 Power cond system': NifCost(base_key='22134PowerCondSystem', procurement=M_USD(98.7), design=M_USD(0.0), assembly=M_USD(0.0)),
    '22.1.3.5 Align and Laser diag': NifCost(base_key='22135AlignAndLaserDiag', procurement=M_USD(71.4), design=M_USD(15.8), assembly=M_USD(48.8)),
    '22.1.3.6 Space frame': NifCost(base_key='22136SpaceFrame', procurement=M_USD(22.5), design=M_USD(3.6), assembly=M_USD(0.0)),
    '22.1.3.7 Laser aux systems': NifCost(base_key='22137LaserAuxSystems', procurement=M_USD(1.5), design=M_USD(0.0), assembly=M_USD(4.0)),
    '22.1.3.8 Optics': NifCost(base_key='22138Optics', procurement=M_USD(0.0), design=M_USD(0.0), assembly=M_USD(0.0)),
}


def get_nif_scaled_costs(laser_energy: MW, lasers: Lasers) -> dict[str, NifCost]:
    # scales for system energy and learning curve
    scaling_factor = laser_energy / lasers.nif_laser_energy * (laser_energy / lasers.nif_laser_energy) ** lasers.beamlet_learning_curve_coefficient_b
    return {title: NifCost(base_key=cost.base_key, procurement=M_USD(scaling_factor * cost.procurement),
                           design=M_USD(scaling_factor * cost.design), assembly=M_USD(scaling_factor * cost.assembly))
            for (title, cost) in NIF_COSTS.items()}


@dataclass
class NifOpticsCost():
    full_system: M_USD
    beamlet: M_USD


# TODO currently these are not used
# Optics NIF subsystem breakdown, totals only, see
# https://docs.google.com/spreadsheets/d/1sMNzOweYvZCR1BeCXR4IciHEikYyZ0a11XpnLshR6DU/edit#gid=1467969509
# for more detail
NIF_OPTICS_COSTS = {
    "Laser glass slabs (phosphate)": NifOpticsCost(full_system=M_USD(121.50356), beamlet=M_USD(419.2936)),
    "Spatial filter lenses (SiO2)": NifOpticsCost(full_system=M_USD(18.063248), beamlet=M_USD(62.2856)),
    "Final focus lenses (SiO2)": NifOpticsCost(full_system=M_USD(5.599344), beamlet=M_USD(19.2708)),
    "Vacuum windows (SiO2)": NifOpticsCost(full_system=M_USD(4.898472), beamlet=M_USD(16.9176)),
    "Debris shields (SiO2)": NifOpticsCost(full_system=M_USD(4.947232), beamlet=M_USD(17.0872)),
    "Pockels cell windows (SiO2)": NifOpticsCost(full_system=M_USD(7.188708), beamlet=M_USD(24.7828)),
    "Polariser (HiQ BK7)": NifOpticsCost(full_system=M_USD(13.7853), beamlet=M_USD(47.5516)),
    "Doubler crystal (KDP)": NifOpticsCost(full_system=M_USD(5.996844), beamlet=M_USD(20.6912)),
    "Tripler crystal (KDP)": NifOpticsCost(full_system=M_USD(12.533864), beamlet=M_USD(43.248)),
    "PC crystal (KDP)": NifOpticsCost(full_system=M_USD(14.940912), beamlet=M_USD(51.5584)),
    "Cavity mirrors (BK7)": NifOpticsCost(full_system=M_USD(11.91652), beamlet=M_USD(41.1068)),
    "Transport mirrors (BK7)": NifOpticsCost(full_system=M_USD(11.960616), beamlet=M_USD(41.2552)),
    "Elbow mirrors (BK7)": NifOpticsCost(full_system=M_USD(6.471088), beamlet=M_USD(22.3236)),
    "Totals": NifOpticsCost(full_system=M_USD(239.805708), beamlet=M_USD(827.3724))
}


def get_nif_replacements(scaled_costs: dict[str, NifCost]) -> dict[str, str]:
    replacements = {}
    for nif_cost in scaled_costs.values():
        replacements[nif_cost.base_key + 'Procurement'] = str(round(nif_cost.procurement, 1))
        replacements[nif_cost.base_key + 'Design'] = str(round(nif_cost.design, 1))
        replacements[nif_cost.base_key + 'Assembly'] = str(round(nif_cost.assembly, 1))
        replacements[nif_cost.base_key + 'Total'] = str(round(nif_cost.total, 1))
    return replacements
