from rdkit.Chem import Descriptors, Descriptors3D, Lipinski, GraphDescriptors, MolSurf, rdMolDescriptors
from mordred import (Calculator, Weight, HydrogenBond, Aromatic, RotatableBond, CarbonTypes,
                     BondCount, RingCount, BalabanJ, BertzCT, KappaShapeIndex, MoeType, EState,
                     McGowanVolume, ExtendedTopochemicalAtom, TopologicalIndex, VdwVolumeABC)
import mordred
from mordred import AtomCount as AtomCount_
from mordred import Polarizability as Polarizability_

def MW(type):
    if type == 'a':
        return Calculator(Weight.Weight(averaged=True))
    elif type == 'e':
        return Calculator(Weight.Weight(averaged=False))

def AtomCount(atom):
    if atom == 'Hetero':
        return rdMolDescriptors.CalcNumHeteroatoms
    elif atom == 'NHOH':
        return Lipinski.NHOHCount
    elif atom == 'NO':
        return Lipinski.NOCount
    elif atom == 'Hdonors':
        return Calculator(HydrogenBond.HBondDonor)
    elif atom == 'Hacceptors':
        return Calculator(HydrogenBond.HBondAcceptor)
    return Calculator(AtomCount_.AtomCount(atom))

def ElecCount(type):
    if type == 'Valence':
        return Descriptors.NumValenceElectrons
    elif type == 'Radical':
        return Descriptors.NumRadicalElectrons
    
def TPSA():
    return MolSurf.TPSA

def EtaCoreCount(*args, **kwargs):       
    return Calculator(ExtendedTopochemicalAtom.EtaCoreCount(*args, **kwargs))

def EtaShapeIndex(*args, **kwargs):
    return Calculator(ExtendedTopochemicalAtom.EtaShapeIndex(*args, **kwargs))

def EtaVEMCount(*args, **kwargs):
    return Calculator(ExtendedTopochemicalAtom.EtaVEMCount(*args, **kwargs))

def EtaCompositeIndex(*args, **kwargs):
    return Calculator(ExtendedTopochemicalAtom.EtaCompositeIndex(*args, **kwargs))

def EtaFunctionalityIndex(*args, **kwargs):
    return Calculator(ExtendedTopochemicalAtom.EtaFunctionalityIndex(*args, **kwargs))

def EtaBranchingIndex(*args, **kwargs):
    return Calculator(ExtendedTopochemicalAtom.EtaBranchingIndex(*args, **kwargs))

def EtaDeltaAlpha(*args, **kwargs):
    return Calculator(ExtendedTopochemicalAtom.EtaDeltaAlpha(*args, **kwargs))

def EtaEpsilon(*args, **kwargs):
    return Calculator(ExtendedTopochemicalAtom.EtaEpsilon(*args, **kwargs))

def EtaDeltaEpsilon(*args, **kwargs):
    return Calculator(ExtendedTopochemicalAtom.EtaDeltaEpsilon(*args, **kwargs))

def EtaDeltaBeta(*args, **kwargs):
    return Calculator(ExtendedTopochemicalAtom.EtaDeltaBeta(*args, **kwargs))

def EtaPsi(*args, **kwargs):
    return Calculator(ExtendedTopochemicalAtom.EtaPsi(*args, **kwargs))

def EtaDeltaPsi(*args, **kwargs):
    return Calculator(ExtendedTopochemicalAtom.EtaDeltaPsi(*args, **kwargs)) 

def Radius():
    return Calculator(TopologicalIndex.Radius)

def TopologicalShapeIndex():
    return Calculator(TopologicalIndex.TopologicalShapeIndex)

def PetitjeanIndex():
    return Calculator(TopologicalIndex.PetitjeanIndex)

def Diameter():
    return Calculator(TopologicalIndex.Diameter)

def VABC():
    return Calculator(VdwVolumeABC.VdwVolumeABC)

def Asphericity():
    return Descriptors3D.Asphericity

def Eccentricity():
    return Descriptors3D.Eccentricity

def InertialShapeFactor():
    return Descriptors3D.InertialShapeFactor

def NPR(ratio):
    if ratio == 1:
        return rdMolDescriptors.CalcNPR1
    elif ratio == 2:
        return rdMolDescriptors.CalcNPR2

def PBF():
    return rdMolDescriptors.CalcPBF

def PMI(order):
    if order == 1:
        return rdMolDescriptors.CalcPMI1
    elif order == 2:
        return rdMolDescriptors.CalcPMI2
    elif order == 3:
        return rdMolDescriptors.CalcPMI3

def SpherocityIndex():
    return rdMolDescriptors.CalcSpherocityIndex

def Kappa(index):
    if index == 1:
        return Calculator(KappaShapeIndex.KappaShapeIndex1)
    elif index == 2:
        return Calculator(KappaShapeIndex.KappaShapeIndex2)
    elif index == 3:
        return Calculator(KappaShapeIndex.KappaShapeIndex3)

def McGowan():
    return Calculator(McGowanVolume.McGowanVolume)

def LabuteASA():
    return Calculator(MoeType.LabuteASA)

def PEOE_VSA(index):
    return Calculator(MoeType.PEOE_VSA(index))

def SMR_VSA(index):
    return Calculator(MoeType.SMR_VSA(index))

def SlogP_VSA(index):
    return Calculator(MoeType.SlogP_VSA(index))

def EState_VSA(index):
    return Calculator(MoeType.EState_VSA(index))

def VSA_EState(index):
    return Calculator(MoeType.VSA_EState(index))

def HybRatio():
    return Calculator(CarbonTypes.HybridizationRatio)

def Carbon(*args, **kwargs):
    return Calculator(CarbonTypes.CarbonTypes(*args, **kwargs))

def Charge(type):
    if type == 'EEM':
        return rdMolDescriptors.CalcEEMcharges
    elif type == 'MaxAbsPartialCharge':
        return Descriptors.MaxAbsPartialCharge
    elif type == 'MaxPartialCharge':
        return Descriptors.MaxPartialCharge
    elif type == 'MinAbsPartialCharge':
        return Descriptors.MinAbsPartialCharge
    elif type == 'MinPartialCharge':
        return Descriptors.MinPartialCharge

def Polarizability(type):
    if type == 'atom':
        return Calculator(Polarizability_.APol())
    elif type == 'bond':
        return Calculator(Polarizability_.BPol())

def AtomTypeEState(*args, **kwargs):
    return Calculator(EState.AtomTypeEState(*args, **kwargs))