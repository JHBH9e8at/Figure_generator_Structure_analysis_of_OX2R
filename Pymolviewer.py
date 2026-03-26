# code for the Figures : code written by JungHyun(Andy) Bang
# Date of creation: 15-03-25
# Date of lats update: 25-03-25
#########################################################################################################
# additional codes and history of development                                                           #
# can be veiwd at: https://github.com/JHBH9e8at/Figure_generator_Structure_analysis_of_OX2R/            #
#########################################################################################################

import sys
from pathlib import Path
import pymol

cmd.reinitialize()
cmd.run("info.py")      # import scrip doesnt work like normal .py cmd runs will run on pymol

def get_model_path(root: Path, subdirs: list[str]) -> list[Path]:
    return [next((root / subdir).glob("*_model_0.cif"))for subdir in subdirs]


def load_models(model_paths: list[Path], object_names: list[str]) -> None:
    if len(model_paths) != len(object_names):
        raise ValueError(f"Length mismatch: {len(model_paths)=}, {len(object_names)=}")

    for model_path, obj_name in zip(model_paths, object_names):
        cmd.load(str(model_path), obj_name)

def load_reference_objects(inactive_path: str, active_path: str) -> None:
    cmd.load(inactive_path, "inactive")
    cmd.load(active_path, "active")
    cmd.align("active", "inactive")


def align_models_to_reference(object_names: list[str], reference: str = "inactive") -> None:
    for obj_name in object_names:
        cmd.align(obj_name, reference)


def init_session() -> None:
    cmd.reinitialize()


def combbmods() -> dict[str, list[str]]:
    init_session()

    nt_model_paths = get_model_path(flexiroot, subdirs_nt)
    wt_model_paths = get_model_path(flexiroot, subdirs_wt)

    load_reference_objects(inap, actp)

    load_models(nt_model_paths, targn_nt)
    load_models(wt_model_paths, targn_wt)

    all_objects = targn_nt + targn_wt
    align_models_to_reference(all_objects, reference="inactive")

    return {"nt": targn_nt,"wt": targn_wt,"all": all_objects}


def selector() -> None:
    for obj, roles in chain_roles.items():
        if "receptor" in roles:
            rec_chain = roles["receptor"]
            if cmd.count_atoms(f"{obj} and chain {rec_chain}") > 0:
                cmd.select(f"{obj}_receptor", f"{obj} and chain {rec_chain}")

        if "gprot" in roles:
            gp_chain = roles["gprot"]
            if cmd.count_atoms(f"{obj} and chain {gp_chain}") > 0:
                cmd.select(f"{obj}_gprot", f"{obj} and chain {gp_chain}")

        if "ligand" in roles:
            lig_chain = roles["ligand"]
            if cmd.count_atoms(f"{obj} and chain {lig_chain}") > 0:
                cmd.select(f"{obj}_ligand", f"{obj} and chain {lig_chain}")


def build_TM_selections() -> None:
    for obj in totlist:
        if cmd.count_atoms(f"{obj} and chain A") > 20:
            chain_id = "A"
        elif cmd.count_atoms(f"{obj} and chain R") > 20:
            chain_id = "R"
        else:
            continue

        for tm_name, (start, end) in TM_ranges.items():
            cmd.select(f"{obj}_{tm_name}",f"{obj} and chain {chain_id} and resi {start}-{end}")


def grouping() -> None:
    cmd.select("gprot_all", "*_gprot")
    cmd.select("ligand_all","*_ligand")
    cmd.select("TM1_all","*_TM1")
    cmd.select("TM2_all","*_TM2")
    cmd.select("TM3_all","*_TM3")
    cmd.select("TM4_all","*_TM4")
    cmd.select("TM5_all","*_TM5")
    cmd.select("TM6_all","*_TM6")
    cmd.select("TM7_all","*_TM7")
    cmd.select("VI1_all","*_viewint1")
    



def initview() -> None:
    cmd.show("cartoon","all")
    cmd.hide("everything", "all")

    cmd.color("marine","all")
    cmd.color(inactive_colour, "inactive")
    cmd.color(active_colour, "active")
    cmd.set("cartoon_color", "yellow", "ligand_all")
    cmd.set("cartoon_color", "red", "active_ligand")

    cmd.set("transparency_mode", 1)
    cmd.set_view(viewcor)




### initblock
obj_registry = combbmods()
totlist = obj_registry["all"]

print("token SE0, Init_comp")

selector()
build_TM_selections()
grouping()
initview()

##3Exp block


def has_ligand(obj: str) -> bool:
    return "L" in obj

def targviewer1(primtarg: str, sectarg: str, bench: str) -> None:
    initview()
    cmd.set_view(viewcor2)
    cmd.show("cartoon", f"{primtarg} {sectarg} {bench}")

    cmd.hide("cartoon", "gprot_all")
    cmd.hide("cartoon", "ligand_all")
    cmd.hide("sticks","ligand_all")

    p_has_L = has_ligand(primtarg)
    s_has_L = has_ligand(sectarg)

    if p_has_L:
        cmd.show("sticks", f"{primtarg}_ligand")
        cmd.set("cartoon_transparency", 0.66, f"{primtarg}_ligand")

    if s_has_L:
        cmd.show("sticks", f"{sectarg}_ligand")
        cmd.set("cartoon_transparency", 0.66, f"{sectarg}_ligand")

    cmd.show("sticks", f"{bench}_ligand")
    cmd.set("cartoon_transparency", 0.66, f"{bench}_ligand")
    cmd.color("red", f"{bench}_ligand")

    cmd.color(f"{primtarg_colour}", f"{primtarg}")
    cmd.set("cartoon_transparency", 0.3, primtarg)
    cmd.set("cartoon_transparency", 0.5, sectarg)
    cmd.set("cartoon_transparency", 0.5, bench)
    cmd.set("stick_transparency", 0.5)

    cmd.hide("cartoon", f"{primtarg}_TM1 {primtarg}_TM2 {primtarg}_TM3 {primtarg}_TM5")
    cmd.hide("cartoon", f"{sectarg}_TM1 {sectarg}_TM2 {sectarg}_TM3 {sectarg}_TM5")
    cmd.hide("cartoon", "VI1_all")



def bpview(primtarg: str, sectarg: str, bench: str) -> None:

    cmd.set_view(viewcor3)

    cmd.hide("sticks","ligand_all")
    cmd.show("cartoon", f"{primtarg}_TM1 {primtarg}_TM2 {primtarg}_TM3 {primtarg}_TM5")
    cmd.show("cartoon", f"{sectarg}_TM1 {sectarg}_TM2 {sectarg}_TM3 {sectarg}_TM5")
    cmd.show("cartoon", "VI1_all")

    cmd.select(f"{primtarg}_inter_resi", f"{primtarg} and chain A and resi 86+276+295+298+302+306")
    cmd.select(f"{sectarg}_inter_resi", f"{sectarg} and chain A and resi 86+276+295+298+302+306")
    cmd.select(f"{bench}_inter_resi", f"{bench} and chain R and resi 134+324+343+346+350+354")
    cmd.select(f"inactive_inter_resi", f"inactive and chain A and resi 134+324+343+346+350+354")
    cmd.show("sticks", f"{primtarg}_inter_resi")
    cmd.show("sticks", f"{sectarg}_inter_resi")
    cmd.show("sticks", f"{bench}_inter_resi")
    cmd.show("sticks", f"inactive_inter_resi")         
    cmd.set("stick_transparency", 0.1, "inactive_inter_resi") 
    cmd.set("stick_transparency", 0.3, f"{sectarg}_inter_resi") 
    cmd.set("stick_transparency", 0.3, f"{primtarg}_inter_resi") 
    cmd.set("stick_transparency", 0.1, "inactive_inter_resi") 
      

    cmd.select(f"{primtarg}_confers", f"{primtarg} and chain A and resi 143-169")            # ECL2 prortion
    cmd.select(f"{sectarg}_confers", f"{sectarg} and chain A and resi 143-169")            # ECL2 prortion
    cmd.select(f"{bench}_confers", f"{bench} and chain R and resi 190-219")  
    cmd.hide("cartoon", f"{primtarg}_confers")
    cmd.hide("cartoon", f"{sectarg}_confers")
    cmd.hide("cartoon", f"{bench}_confers")
    cmd.hide("everything", "ligand_all")
    cmd.set("stick_transparency", 0.1)


    cmd.hide("cartoon", f"{primtarg}_TM1 {primtarg}_TM4 ")
    cmd.hide("cartoon", f"{sectarg}_TM1 {sectarg}_TM4 ")
    
    p_has_L = has_ligand(primtarg)
    s_has_L = has_ligand(sectarg)

    if p_has_L:
        cmd.show("cartoon", f"{primtarg}_ligand")
        cmd.set("cartoon_transparency", 0.66, f"{primtarg}_ligand")

    if s_has_L:
        cmd.show("cartoon", f"{sectarg}_ligand")
        cmd.set("cartoon_transparency", 0.66, f"{sectarg}_ligand")

    cmd.show("cartoon", f"{bench}_ligand")
    cmd.set("cartoon_transparency", 0.66, f"{bench}_ligand")
    cmd.set("cartoon_color", "red", f"{bench}_ligand")

    

def take_pic(outname:str):
    cmd.set("transparency_mode", 3)
    cmd.set("ray_shadows", 0)
    cmd.set("ray_trace_gain", 0)
    cmd.ray(1200,1200)
    cmd.png(f"{outname}")
    cmd.set("transparency_mode", 1)

def addi():
    cmd.hide("everything", "ligand_all")
    vv1 = (0.679800928,   -0.628223300,    0.378304064,\
    -0.169742242,    0.367037088,    0.914555788,\
    -0.713418126,   -0.685958862,    0.142899200,\
    -0.004963852,   -0.003032899,  -30.073497772,\
    88.614433289,  218.069580078,    5.491996765,\
   -26.714403152,   75.353157043,  -20.000000000 )
    cmd.set_view(vv1)
    

# exp_comb ={
#     "G_EFF_WT_LIG_OFF":["wt_RG","wt_R","active"],
#     "L_EFF_WT_GP_ON":["wt_RGL","wt_RG","active"],    
#            }

for exp_name, (primtar,sectar,ref) in exp_comb.items():
    targviewer1(primtar,sectar,ref)
    # take_pic(f"{exp_name}_1")
    bpview(primtar,sectar,ref)
    addi()
    # take_pic(f"{exp_name}_Close")