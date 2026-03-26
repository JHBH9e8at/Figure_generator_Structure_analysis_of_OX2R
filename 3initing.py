from pathlib import Path
from pymol import cmd

viewcor = (\
    -0.765872359,    0.147503078,   -0.625838757,\
     0.089428134,    0.988301635,    0.123493634,\
     0.636738718,    0.038614605,   -0.770110309,\
     0.000899865,   -0.002091363, -331.043853760,\
    94.755088806,  197.821853638,    3.936901093,\
   283.857818604,  378.081939697,  -20.000000000 )
inap = r"C:\Users\1\OneDrive\QMUL\sem2\704_Datadriven\labs\week5\LABFILES\6TPN_Inactive.pdb"
actp = r"C:\Users\1\OneDrive\QMUL\sem2\704_Datadriven\labs\week5\LABFILES\7L1U_Active.pdb"

flexiroot = Path(r"C:\Users\1\OneDrive\QMUL\sem2\704_Datadriven\labs\week5\Results\AF3_1_nt")

out_dir = r"C:\Users\1\OneDrive\QMUL\sem2\704_Datadriven\labs\week5\Results\Figures"


subdirs = [
    "fold_ox2r_notemplates",
    "fold_ox2r_notemplates_g_prot",
    "fold_ox2r_notemplates_g_prot_orxb",
    "fold_ox2r_notemplates_orxb",
]




def runexp(flexiroot, sub, out_dir):
    cif_files = sorted((flexiroot / sub).glob("*_model_*.cif"))
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
        break


    cmd.align("active and name CA", "inactive and name CA", cycles=0)

    for obj_name in models:
        cmd.align(f"{obj_name} and name CA","inactive and name CA", cycles=0)
        cmd.color("marine", obj_name)
        cmd.set("cartoon_transparency", 0.8, obj_name)
        cmd.set("cartoon_transparency",0.9, "chain B")
        cmd.set("cartoon_transparency",0.3, "chain C")

    # #testing

    # cmd.set("cartoon_transparency", 0.3, models[1])

    cmd.set_view(viewcor)

    # for obj_name in models:
    #     cmd.set("cartoon_transparency", 0.3, obj_name)
    #     # print(obj_name) = fold_ox2r_notemplates_g_prot_orxb_model_4
    #     outfile = f"{out_dir}\\{obj_name}.png"
    #     cmd.png(outfile, width=2000, height=2000, dpi=300, ray=0)
    #     cmd.set("cartoon_transparency", 0.8, obj_name)        


for i in subdirs:
    runexp(flexiroot,i,out_dir)

    