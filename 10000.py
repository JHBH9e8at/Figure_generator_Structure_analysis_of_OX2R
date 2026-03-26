from pathlib import Path
from pymol import cmd
import os


viewcor = (-0.765872359, 0.147503078, -0.625838757,
           0.089428134, 0.988301635, 0.123493634,
           0.636738718, 0.038614605, -0.770110309,
           0.000899865, -0.002091363, -331.043853760,
           94.755088806, 197.821853638, 3.936901093,
           283.857818604, 378.081939697, -20.000000000)


inap = r"C:\Users\1\OneDrive\QMUL\sem2\704_Datadriven\labs\week5\LABFILES\6TPN_Inactive.pdb"
actp = r"C:\Users\1\OneDrive\QMUL\sem2\704_Datadriven\labs\week5\LABFILES\7L1U_Active.pdb"

flexiroot = Path(r"C:\Users\1\OneDrive\QMUL\sem2\704_Datadriven\labs\week5\Results\AF3_1_nt")
out_dir = Path(r"C:\Users\1\OneDrive\QMUL\sem2\704_Datadriven\labs\week5\Results\Figures")

subdirs = [
    "fold_ox2r_notemplates",
    "fold_ox2r_notemplates_g_prot",
    "fold_ox2r_notemplates_g_prot_orxb",
    "fold_ox2r_notemplates_orxb",
]

targn1 = ["R","RG","RGL","RL"]

cmd.reinitialize()
def runs(flexiroot=flexiroot, sub_dir=subdirs):

    targs = []
    for i in sub_dir:
        p = flexiroot / i
        cif_f = sorted(p.glob("*_model_*.cif"))
        if cif_f:
            targs.append(cif_f[0])

    return targs

targs =runs()

def loadinginst(targlist=targs,targn=targn):
    cmd.load(inap, "inactive")
    cmd.load(actp, "active")
    for i, name in zip(targlist, targn):
        cmd.load(str(i), name)

loadinginst()

for name in targn:
    cmd.align("active","inactive")
    cmd.align(name,"inactive")

# loading all mods comp.


cmd.set("cartoon_transparency", 0.9,"all")
cmd.set("cartoon_transparency", 0.7,"active inactive")

cmd.set("cartoon_transparency", 0.5,"R")

cmd.color("marine", "all")
cmd.color("red", "active")
cmd.color("grey70", "inactive")
cmd.orient("active")



