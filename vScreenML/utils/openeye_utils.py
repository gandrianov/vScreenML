import sys
from openeye import oechem
from openeye import oequacpac

def AssignChargesByName(mol, name):
    if name == "noop":
        return oequacpac.OEAssignCharges(mol, oequacpac.OEChargeEngineNoOp())
    elif name == "mmff" or name == "mmff94":
        return oequacpac.OEAssignCharges(mol, oequacpac.OEMMFF94Charges())
    elif name == "am1bcc":
        return oequacpac.OEAssignCharges(mol, oequacpac.OEAM1BCCCharges())
    elif name == "am1bccnosymspt":
        optimize = True
        symmetrize = True
        return oequacpac.OEAssignCharges(mol, oequacpac.OEAM1BCCCharges(not optimize, not symmetrize))
    elif name == "amber" or name == "amberff94":
        return oequacpac.OEAssignCharges(mol, oequacpac.OEAmberFF94Charges())
    elif name == "am1bccelf10":
        return oequacpac.OEAssignCharges(mol, oequacpac.OEAM1BCCELF10Charges())
    return False


def main(argv=[__name__]):
    itf = oechem.OEInterface(InterfaceData)

    if not oechem.OEParseCommandLine(itf, argv):
        oechem.OEThrow.Fatal("Unable to interpret command line!")

    ifs = oechem.oemolistream()

    inputFile = itf.GetString("-in")
    if not ifs.open(inputFile):
        oechem.OEThrow.Fatal("Unable to open %s for reading" % inputFile)

    ofs = oechem.oemolostream()
    ofs.SetFormat(oechem.OEFormat_MOL2)
    ofs.openstring()

    fwr = open(itf.GetString("-out"), "w")

    chargeName = itf.GetString("-method")

    mol = oechem.OEMol()
    while oechem.OEReadMolecule(ifs, mol):

        if not AssignChargesByName(mol, chargeName):
            oechem.OEThrow.Warning("Unable to assign %s charges to mol %s"
                                   % (chargeName, mol.GetTitle()))
        oechem.OEWriteMolecule(ofs, mol)

        oechem.OECanonicalOrderAtoms(mol)
        oechem.OECanonicalOrderBonds(mol)
        oechem.OEClearAromaticFlags(mol)
        oechem.OEKekulize(mol)

        smi = oechem.OECreateSmiString(mol, oechem.OESMILESFlag_Canonical | oechem.OESMILESFlag_Hydrogens)

        mol2 = str(ofs.GetString().decode('utf-8')).split("\n")
        mol2[1] += " " + smi
        mol2 = "\n".join(mol2)

        fwr.write(mol2)
        fwr.close()


    ifs.close()
    ofs.close()



#############################################################################
# INTERFACE
#############################################################################


InterfaceData = '''
!BRIEF AssignCharges.py [-options] <inmol> [<outmol>]

!CATEGORY "input/output options :"
   !PARAMETER -in
      !ALIAS -i
      !TYPE string
      !BRIEF Input molecule
      !VISIBILITY simple
      !REQUIRED true
      !KEYLESS 1
   !END

   !PARAMETER -out
      !ALIAS -o
      !TYPE string
      !DEFAULT oeassigncharges.oeb.gz
      !BRIEF Output molecule (usually an oeb)
      !VISIBILITY simple
      !REQUIRED false
      !KEYLESS 2
   !END
!END

!CATEGORY "Charging options :"
   !PARAMETER -method
      !TYPE string
      !LEGAL_VALUE noop
      !LEGAL_VALUE mmff
      !LEGAL_VALUE mmff94
      !LEGAL_VALUE am1bcc
      !LEGAL_VALUE am1bccnosymspt
      !LEGAL_VALUE amber
      !LEGAL_VALUE amberff94
      !LEGAL_VALUE am1bccelf10
      !DEFAULT mmff94
      !BRIEF which set of charges to apply
      !SIMPLE true
      !REQUIRED false
   !END
!END
'''


def assign_charges():
    sys.exit(main(sys.argv))
    
