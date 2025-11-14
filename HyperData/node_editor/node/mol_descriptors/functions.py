from rdkit.Chem import Descriptors, Descriptors3D, Lipinski, GraphDescriptors, MolSurf, EState
from mordred import (Calculator, Weight, AtomCount, HydrogenBond, Aromatic, RotatableBond,
                     BondCount, RingCount, BalabanJ, BertzCT, KappaShapeIndex, MoeType,
                     McGowanVolume, ExtendedTopochemicalAtom, TopologicalIndex, VdwVolumeABC)

def MW(type):
    if type == 'a':
        try:
            return Calculator(Weight.Weight(False))
        except:
            return Descriptors.MolWt
    elif type == 'e':
        try:
            return Calculator(Weight.Weight(True))
        except:
            return Descriptors.ExactMolWt
    elif type == 'h':
        return Descriptors.HeavyAtomMolWt

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
    try:
        return Calculator(TopologicalIndex.TopologicalShapeIndex)
    except:
        return Descriptors3D.RadiusOfGyration

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
        return Descriptors3D.NPR1
    elif ratio == 2:
        return Descriptors3D.NPR2

def PBF():
    return Descriptors3D.PBF

def PMI(order):
    if order == 1:
        return Descriptors3D.PMI1
    elif order == 2:
        return Descriptors3D.PMI2
    elif order == 3:
        return Descriptors3D.PMI3

def SpherocityIndex():
    return Descriptors3D.SpherocityIndex

def Kappa(index):
    if index == 1:
        try:
            return GraphDescriptors.Kappa1
        except:
            return Calculator(KappaShapeIndex.KappaShapeIndex1)
    elif index == 2:
        try:
            return GraphDescriptors.Kappa2
        except:
            return Calculator(KappaShapeIndex.KappaShapeIndex2)
    elif index == 3:
        try:
            return GraphDescriptors.Kappa3
        except:
            return Calculator(KappaShapeIndex.KappaShapeIndex3)