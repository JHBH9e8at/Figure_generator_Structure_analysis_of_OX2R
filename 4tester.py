from pathlib import Path
from pymol import cmd

viewcor = (
    -0.765872359, 0.147503078, -0.625838757,
     0.089428134, 0.988301635, 0.123493634,
     0.636738718, 0.038614605, -0.770110309,
     0.000899865, -0.002091363, -331.043853760,
    94.755088806, 197.821853638, 3.936901093,
   283.857818604, 378.081939697, -20.000000000
)

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


def runexp(flexiroot, sub, out_dir):
    cif_files = sorted((flexiroot / sub).glob("*_model_*.cif"))
    out_dir.mkdir(parents=True, exist_ok=True)

    cmd.reinitialize()
    cmd.load(inap, "inactive")
    cmd.load(actp, "active")

    cmd.color("red", "active")
    cmd.color("grey70", "inactive")
    cmd.set("cartoon_transparency", 0.5, "active")
    cmd.set("cartoon_transparency", 0.5, "inactive")

    models = []
    for cif_file in cif_files:
        obj_name = cif_file.stem
        cmd.load(str(cif_file), obj_name)
        models.append(obj_name)

    cmd.align("active and name CA", "inactive and name CA", cycles=0)

    for obj_name in models:
        cmd.align(f"{obj_name} and name CA", "inactive and name CA", cycles=0)
        cmd.color("marine", obj_name)
        cmd.set("cartoon_transparency", 0.8, obj_name)

    
    cmd.set("cartoon_transparency", 0.9, "chain B")
    cmd.set("cartoon_transparency", 0.3, "chain C")
    cmd.color("yellow", "chain C")

    cmd.set_view(viewcor)

    for obj_name in models:
        cmd.set("cartoon_transparency", 0.3, obj_name)

        
        cmd.set("cartoon_transparency", 0.9, f"{obj_name} and chain B")
        cmd.set("cartoon_transparency", 0.3, f"{obj_name} and chain C")

        outfile = out_dir / f"{obj_name}.png"
        cmd.ray(1500,1500)
        cmd.png(str(outfile))


        #REV FOR NEXT LP
        cmd.set("cartoon_transparency", 0.8, obj_name)
        cmd.set("cartoon_transparency", 0.9, f"{obj_name} and chain B")
        cmd.set("cartoon_transparency", 0.3, f"{obj_name} and chain C")

for sub in subdirs:
    runexp(flexiroot, sub, out_dir)