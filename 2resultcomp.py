import pymol
from pymol import cmd

viewcor = (-0.892409086227417, 0.05872834101319313, -0.44737958908081055, -0.006947621703147888, 0.9895830154418945, 0.14376288652420044, 0.4511653780937195, 0.13140623271465302, -0.8827118277549744, 0.0008369907736778259, -0.0018610060214996338, -314.1247253417969, 96.10614013671875, 201.17279052734375, 3.8829193115234375, 266.9494323730469, 361.1735534667969, -20.0)

pymol.finish_launching()

cmd.reinitialize()

inap = r"C:\Users\1\OneDrive\QMUL\sem2\704_Datadriven\labs\week5\LABFILES\6TPN_Inactive.pdb"
actp = r"C:\Users\1\OneDrive\QMUL\sem2\704_Datadriven\labs\week5\LABFILES\7L1U_Active.pdb"


str0 = r"C:\Users\1\OneDrive\QMUL\sem2\704_Datadriven\labs\week5\Results\1_wt\fold_ox2r_with_templates_gp\fold_ox2r_with_templates_gp_model_0.cif"
str1 = r"C:\Users\1\OneDrive\QMUL\sem2\704_Datadriven\labs\week5\Results\1_wt\fold_ox2r_with_templates_gp\fold_ox2r_with_templates_gp_model_0.cif"
str2 = r"C:\Users\1\OneDrive\QMUL\sem2\704_Datadriven\labs\week5\Results\1_wt\fold_ox2r_with_templates_gp\fold_ox2r_with_templates_gp_model_0.cif"
str3 = r"C:\Users\1\OneDrive\QMUL\sem2\704_Datadriven\labs\week5\Results\1_wt\fold_ox2r_with_templates_gp\fold_ox2r_with_templates_gp_model_0.cif"
str4 = r"C:\Users\1\OneDrive\QMUL\sem2\704_Datadriven\labs\week5\Results\1_wt\fold_ox2r_with_templates_gp\fold_ox2r_with_templates_gp_model_0.cif"




cmd.load(inap, "inactive")
cmd.load(actp, "active")

cmd.load(str0, "str0")
cmd.load(str1, "str1")
cmd.load(str2, "str2")
cmd.load(str3, "str3")
cmd.load(str4, "str4")

cmd.align("active and name CA", "inactive and name CA", cycles=0)
cmd.align("str0 and name CA", "inactive and name CA", cycles=0)
cmd.align("str1 and name CA", "inactive and name CA", cycles=0)
cmd.align("str2 and name CA", "inactive and name CA", cycles=0)
cmd.align("str3 and name CA", "inactive and name CA", cycles=0)
cmd.align("str4 and name CA", "inactive and name CA", cycles=0)

cmd.orient("inactive")

cmd.color("red", "active")
cmd.color("grey70", "inactive")
cmd.color("marine", "str0 str1 str2 str3 str4")

cmd.set("cartoon_transparency", 0.5, "active")
cmd.set("cartoon_transparency", 0.5, "inactive")
cmd.set("cartoon_transparency", 0.7, "str1 str2 str3 str4")

cmd.set("cartoon_transparency", 0.8, "str0 and chain B")




cmd.select("str0_highrmsdreg", "str0 and resi 205-232 and name CA")
cmd.select("str1_highrmsdreg", "str1 and resi 205-232 and name CA")
cmd.select("str2_highrmsdreg", "str2 and resi 205-232 and name CA")
cmd.select("str3_highrmsdreg", "str3 and resi 205-232 and name CA")
cmd.select("str4_highrmsdreg", "str4 and resi 205-232 and name CA")
cmd.set_view(viewcor)


# models = ["str0","str1","str2","str3","str4"]
# outdir = r"C:\Users\1\OneDrive\QMUL\sem2\704_Datadriven\labs\week5\Results\figures\WT\wt_receptoronly"

# for i, m in enumerate(models):
#     for obj in models:
#         cmd.set("cartoon_transparency", 0.7, obj)
#     cmd.set("cartoon_transparency", 0.0, m)
#     cmd.set("cartoon_transparency", 0.5, "active")
#     cmd.set("cartoon_transparency", 0.5, "inactive")
#     cmd.set_view(viewcor)
#     cmd.set("cartoon_transparency", 0.8, f"{m} and chain B")

#     outfile = f"{outdir}\\highlight_{m}.png"
#     cmd.png(outfile, width=2000, height=2000, dpi=300, ray=0)