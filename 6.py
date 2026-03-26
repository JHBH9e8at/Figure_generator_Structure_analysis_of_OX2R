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


def find_peptide_and_gprot_chains(obj_name, peptide_len_cutoff=10):
    """
    Assumption:
      - receptor is chain A
      - peptide is any non-A chain with CA count <= peptide_len_cutoff
      - gprotein is any non-A chain with CA count > peptide_len_cutoff
    """
    receptor_chain = "A"
    peptide_chains = []
    gprot_chains = []

    for ch in cmd.get_chains(obj_name):
        if ch == receptor_chain:
            continue

        n_ca = len(cmd.get_model(f"{obj_name} and chain {ch} and name CA").atom)

        if n_ca <= peptide_len_cutoff:
            peptide_chains.append(ch)
        else:
            gprot_chains.append(ch)

    return receptor_chain, peptide_chains, gprot_chains


def apply_base_render_settings():
    cmd.set("transparency_mode", 3)
    cmd.set("ray_shadows", 0)
    cmd.set("two_sided_lighting", "on")
    cmd.set("depth_cue", 0)
    cmd.set("ray_trace_gain", 0)


def runexp(flexiroot, sub, out_dir):
    cif_files = sorted((flexiroot / sub).glob("*_model_*.cif"))

    this_out = out_dir / sub
    this_out.mkdir(parents=True, exist_ok=True)

    cmd.reinitialize()
    apply_base_render_settings()

    cmd.load(inap, "inactive")
    cmd.load(actp, "active")

    cmd.color("red", "active")
    cmd.color("grey70", "inactive")
    cmd.set("cartoon_transparency", 0.5, "active")
    cmd.set("cartoon_transparency", 0.5, "inactive")

    models = []
    chain_info = {}

    for cif_file in cif_files:
        obj_name = cif_file.stem
        cmd.load(str(cif_file), obj_name)
        models.append(obj_name)

    cmd.align("active and name CA", "inactive and name CA", cycles=0)

    for obj_name in models:
        cmd.align(f"{obj_name} and name CA", "inactive and name CA", cycles=0)
        cmd.color("marine", obj_name)
        cmd.set("cartoon_transparency", 0.8, obj_name)

        receptor_chain, peptide_chains, gprot_chains = find_peptide_and_gprot_chains(
            obj_name, peptide_len_cutoff=10
        )
        chain_info[obj_name] = {"receptor": receptor_chain,
                                "peptides": peptide_chains,
                                "gprots": gprot_chains,}
        for gch in gprot_chains:
            cmd.set("cartoon_transparency", 0.9, f"{obj_name} and chain {gch}")

        for pch in peptide_chains:
            cmd.set("cartoon_transparency", 0.3, f"{obj_name} and chain {pch}")
            cmd.color("yellow", f"{obj_name} and chain {pch}")

    cmd.set_view(viewcor)

    for obj_name in models:
        peptide_chains = chain_info[obj_name]["peptides"]
        gprot_chains = chain_info[obj_name]["gprots"]

        cmd.set("cartoon_transparency", 0.0, obj_name)

        
        for gch in gprot_chains:
            cmd.set("cartoon_transparency", 0.9, f"{obj_name} and chain {gch}")

        for pch in peptide_chains:
            cmd.set("cartoon_transparency", 0.3, f"{obj_name} and chain {pch}")
            cmd.color("yellow", f"{obj_name} and chain {pch}")

        outfile = this_out / f"{obj_name}.png"
        cmd.ray(1500, 1500)
        cmd.png(str(outfile))
        cmd.set("cartoon_transparency", 0.8, obj_name)

        for gch in gprot_chains:
            cmd.set("cartoon_transparency", 0.9, f"{obj_name} and chain {gch}")

        for pch in peptide_chains:
            cmd.set("cartoon_transparency", 0.3, f"{obj_name} and chain {pch}")
            cmd.color("yellow", f"{obj_name} and chain {pch}")


for sub in subdirs:
    runexp(flexiroot, sub, out_dir)



    cmd.select("proxsel", "resn 351 352 353")