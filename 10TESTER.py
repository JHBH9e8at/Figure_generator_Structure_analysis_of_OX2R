from pathlib import Path
from pymol import cmd
import os


viewcor =(\
    -0.683953524,   -0.100280561,   -0.722582579,\
     0.003575432,    0.990022719,   -0.140777990,\
     0.729499936,   -0.098868594,   -0.676790059,\
     0.002987940,   -0.004852675, -319.286651611,\
    95.776885986,  203.602508545,    3.510681152,\
   235.524139404,  402.448211670,  -20.000000000 )

viewcor2= (\
    -0.681777358,   -0.046763659,   -0.730027318,\
    -0.174045801,    0.979648769,    0.099789992,\
     0.710509419,    0.195104152,   -0.676075697,\
     0.007243648,   -0.005984468, -182.807571411,\
    97.317626953,  180.863861084,   -2.615722656,\
    94.189125061,  271.429046631,  -20.000000000 )

viewcor3=(\
     0.723819077,   -0.589098811,    0.359125167,\
     0.070432216,    0.580872357,    0.810909152,\
    -0.686318815,   -0.561681271,    0.461963177,\
    -0.006938800,   -0.005134106,  -77.441123962,\
    89.591644287,  224.543548584,   -3.189865112,\
   -15.229599953,  150.062881470,  -20.000000000 )
inap = r"C:\Users\1\OneDrive\QMUL\sem2\704_Datadriven\labs\week5\LABFILES\6TPN_Inactive.pdb"
actp = r"C:\Users\1\OneDrive\QMUL\sem2\704_Datadriven\labs\week5\LABFILES\7L1U_Active.pdb"

flexiroot = Path(r"C:\Users\1\OneDrive\QMUL\sem2\704_Datadriven\labs\week5\Results")
out_dir = Path(r"C:\Users\1\OneDrive\QMUL\sem2\704_Datadriven\labs\week5\Results\Figures")

subdirs_nt = [
    r"AF3_1_nt\fold_ox2r_notemplates",
    r"AF3_1_nt\fold_ox2r_notemplates_g_prot",
    r"AF3_1_nt\fold_ox2r_notemplates_g_prot_orxb",
    r"AF3_1_nt\fold_ox2r_notemplates_orxb",
]

subdirs_wt = [
    r"AF3_1_wt\fold_ox2r_with_templates",
    r"AF3_1_wt\fold_ox2r_with_templates_gp",
    r"AF3_1_wt\fold_ox2r_with_templates_gp_orxb",
    r"AF3_1_wt\fold_ox2r_with_templates_oxb",
]


targn_nt = ["nt_R","nt_RG","nt_RGL","nt_RL"]
targn_wt = ["wt_R","wt_RG","wt_RGL","wt_RL"]


cmd.reinitialize()

cmd.set("transparency_mode", 1)

cmd.load(inap, "inactive")
cmd.load(actp, "active")
cmd.align("active","inactive")

def runs(flexiroot, subdirs_nt, subdirs_wt):

    targs_nt = []

    for i in subdirs_nt:
        p = flexiroot / i
        cif_f = sorted(p.glob("*_model_*.cif"))
        if cif_f:
            targs_nt.append(cif_f[0])

    targs_wt = []

    for i in subdirs_wt:
        p = flexiroot / i
        cif_f = sorted(p.glob("*_model_*.cif"))
        if cif_f:
            targs_wt.append(cif_f[0])

    return targs_nt, targs_wt


def isntload(file_list, name_list):
    for path, name in zip(file_list, name_list):
        cmd.load(str(path), name)


targs_nt, targs_wt = runs(flexiroot, subdirs_nt, subdirs_wt)
isntload(targs_nt, targn_nt)
isntload(targs_wt, targn_wt)

totlist=targn_nt + targn_wt


for name in totlist:
    cmd.align(name,"inactive")

# loading all mods comp -> 


#colorsoritng 
cmd.color("marine", "all")
cmd.color("red", "active")
cmd.color("grey70", "inactive")
#333#####

cmd.set("cartoon_transparency", 0.9,"all")
cmd.set("cartoon_transparency", 0.6,"active inactive")
receptor_chain = "A"

peptide_chains = {}
gprot_chains = {}

for obj in totlist:
    peptide_chains[obj] = []
    gprot_chains[obj] = []

    for chain in cmd.get_chains(obj):
        if chain == receptor_chain:
            continue

        n_ca = cmd.count_atoms(f"{obj} and chain {chain} and name CA")

        if n_ca <= 10:
            peptide_chains[obj].append(chain)
        else:
            gprot_chains[obj].append(chain)

    if peptide_chains[obj]:
        cmd.select(f"{obj}_peptide", f"{obj} and chain {'+'.join(peptide_chains[obj])}")
    else:
        cmd.select(f"{obj}_peptide","none")


    if gprot_chains[obj]:
        cmd.select(f"{obj}_gprot", f"{obj} and chain {'+'.join(gprot_chains[obj])}")
    else:
        cmd.select(f"{obj}_gprot","none")



cmd.select("Active_peptide", "active and chain L")
cmd.select("gprot_all", "*_gprot")
cmd.select("ligand_all","*_peptide")
cmd.hide("everything", "all")
cmd.color("yellow", "ligand_all")
cmd.color("red", "Active_peptide")
cmd.show("sticks", "ligand_all")
cmd.set("stick_transparency", 0.7, "ligand_all")


cmd.set_view(viewcor)


def base_viewset():
    cmd.set("cartoon_transparency", 0.7, "all")
    cmd.hide("all")


def Gprot_view(target1_G:str, target2_NG:str, bench):
    cmd.set_view(viewcor)
    cmd.show("cartoon", f"{target1_G} {target2_NG} {bench}")
    cmd.color("violet",f"{target1_G}")
    cmd.hide("cartoon", f"{target1_G}_peptide {target2_NG}_peptide Active_peptide")
    cmd.show("sticks", f"{target1_G}_peptide Active_peptide")
    cmd.set("stick_transparency", 0.7, "ligand_all")
    cmd.color("yellow", "ligand_all")
    cmd.color("red", "Active_peptide")
    cmd.hide("cartoon", "gprot_all")
    cmd.set("cartoon_transparency", 0.7,f"{target2_NG}")
    cmd.set("cartoon_transparency", 0.3,f"{target1_G}")
    cmd.set("cartoon_transparency", 0.7,f"{bench}")


def NGprot_view(target1_G:str, target2_NG:str, bench):
    cmd.set_view(viewcor)
    cmd.show("cartoon", f"{target1_G} {target2_NG} {bench}")
    cmd.color("violet",f"{target1_G}")
    cmd.hide("cartoon", f"{target1_G}_peptide {target2_NG}_peptide Active_peptide")
    cmd.show("sticks", f"{target2_NG}_peptide Active_peptide")
    cmd.set("stick_transparency", 0.7, "ligand_all")
    cmd.color("yellow", "ligand_all")
    cmd.color("red", "Active_peptide")
    cmd.hide("cartoon", "gprot_all")
    cmd.set("cartoon_transparency", 0.3,f"{target2_NG}")
    cmd.set("cartoon_transparency", 0.7,f"{target1_G}")
    cmd.set("cartoon_transparency", 0.7,f"{bench}")

def inspectinter(target:str, subtar:str):
    cmd.set_view(viewcor3)

    cmd.set("cartoon_transparency", 0.3,f"{target}")
    cmd.set("cartoon_transparency", 0.3,f"{subtar}")
    cmd.hide("cartoon", "active")

    cmd.select(f"{target}_confres", f"{target} and chain A and resi 143-169")            # ECL2 prortion
    cmd.select(f"{subtar}_confres", f"{subtar} and chain A and resi 143-169")            # ECL2 prortion
    cmd.select("active_confers", "active and chain R and resi 190-213")            # ECL2 prortion

    cmd.hide("cartoon", f"{target}_confres")
    cmd.hide("cartoon", f"{subtar}_confres")
    cmd.hide("cartoon", "active_confers")

    cmd.select(f"{target}_inter_resi", f"{target} and chain A and resi 86+276+295+298+302+306")
    cmd.select(f"{subtar}_inter_resi", f"{subtar} and chain A and resi 86+276+295+298+302+306")
    cmd.select(f"active_inter_resi", f"active and chain R and resi 134+324+343+346+350+354")
        

    cmd.show("sticks", f"{target}_inter_resi")
    cmd.show("sticks", f"{subtar}_inter_resi")
    cmd.show("sticks", f"active_inter_resi")

    cmd.set("stick_transparency", 0.3, f"{target}_inter_resi")
    cmd.set("stick_transparency", 0.3, f"{subtar}_inter_resi")
    cmd.hide("everything", "ligand_all")
    # cmd.util.cba(f"{target}_inter_resi")            ####
    # cmd.util.cba(f"{subtar}_inter_resi")
    cmd.color("atomic", f"({target}_inter_resi) and not elem C")
    cmd.color("atomic", f"({subtar}_inter_resi) and not elem C")


def take_picture(outname:str):
    cmd.set_view(viewcor)
    cmd.set("transparency_mode", 3)
    cmd.set("ray_shadows", 0)
    cmd.set("two_sided_lighting", "on")
    cmd.set("depth_cue", 0)
    cmd.set("ray_trace_gain", 0)
    cmd.ray(1200,1200)
    cmd.png(f"{outname}_1")

    cmd.set_view(viewcor2)
    cmd.set("transparency_mode", 3)
    cmd.set("ray_shadows", 0)
    cmd.set("two_sided_lighting", "on")
    cmd.set("depth_cue", 0)
    cmd.set("ray_trace_gain", 0)
    cmd.ray(1200,1200)
    cmd.png(f"{outname}_2")

    cmd.set("transparency_mode", 1)
    print("Jobdone")

def takeinterpicture(outname:str):
    cmd.set_view(viewcor3)
    cmd.set("transparency_mode", 3)
    cmd.set("ray_shadows", 0)
    cmd.set("two_sided_lighting", "on")
    cmd.set("depth_cue", 0)
    cmd.set("ray_trace_gain", 0)
    cmd.ray(1200,1200)
    cmd.png(f"{outname}_3")
    cmd.set("transparency_mode", 1)


# base_viewset()
# Gprot_view("wt_RGL", "wt_RL", "active")
# take_picture("wt_GP")
# inspectinter("wt_RGL","wt_RL")
# takeinterpicture("wt_GP")
# base_viewset()
# NGprot_view("wt_RGL", "wt_RL", "active")
# take_picture("wt_NGP")
# inspectinter("wt_RL","wt_RGL")
# takeinterpicture("wt_NGP")

# base_viewset()
# Gprot_view("nt_RGL", "nt_RL", "active")
# take_picture("nt_GP")
# inspectinter("nt_RGL","nt_RL")
# takeinterpicture("nt_GP")
# base_viewset()
# NGprot_view("nt_RGL", "nt_RL", "active")
# take_picture("nt_NGP")
# inspectinter("nt_RGL","nt_RL")
# takeinterpicture("nt_NGP")


exp_comb ={"wt_Geffect_Ligand_ON_ref_active":["wt_RGL","wt_RL","active"],
           "nt_Geffect_Ligand_OFF_active":["wt_RG","wt_R","active"],
           "wt_Ligand_Gprot_ON_active":["wt_RGL","wt_RG","active"],
           "nt_Ligand_Gprot_OFF_active":["wt_RL","wt_R","active"]
           }


def full_runexp(indir:dict):
    for exp_name, (primtar,sectar,ref) in indir.items():
        base_viewset()
        Gprot_view(primtar,sectar,ref)
        take_picture(f"{exp_name}")
        inspectinter(primtar,sectar)
        takeinterpicture(f"{exp_name}")

full_runexp(exp_comb)