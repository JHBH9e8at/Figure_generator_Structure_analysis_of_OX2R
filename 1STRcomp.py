import pymol
from pymol import cmd


pymol.finish_launching()

cmd.reinitialize()

cmd.run("angles.py")

inap = r"C:\Users\1\OneDrive\QMUL\sem2\704_Datadriven\labs\week5\LABFILES\6TPN_Inactive.pdb"
actp = r"C:\Users\1\OneDrive\QMUL\sem2\704_Datadriven\labs\week5\LABFILES\7L1U_Active.pdb"

cmd.load(inap, "inactive")
cmd.load(actp, "active")
cmd.align("active", "inactive")
cmd.color("red", "active")
cmd.color("grey70", "inactive")
cmd.set("cartoon_transparency", 0.1, "active")
cmd.set("cartoon_transparency", 0.4, "inactive")

            ######TM3
cmd.select("TM3_active", "active and resi 124-157 and name CA")
cmd.select("TM3_inactive", "inactive and resi 124-157 and name CA")



            ######TM6
cmd.select("TM6a_active", "active and resi 293-314 and name CA")
cmd.select("TM6a_inactive", "inactive and resi 295-313 and name CA")

            ######TM7
cmd.select("TM7a_active", "active and resi 369-376 and name CA")
cmd.select("TM7b_active", "active and resi 357-367 and name CA")

cmd.select("TM7a_inactive", "inactive and resi 369-384 and name CA")
cmd.select("TM7b_inactive", "inactive and resi 357-367 and name CA")



cmd.do("cafit_orientation TM3_active, visualize=1")
cmd.do("cafit_orientation TM3_inactive, visualize=1")
cmd.do("cafit_orientation TM6a_active, visualize=1")
cmd.do("cafit_orientation TM6a_inactive, visualize=1")
cmd.do("cafit_orientation TM7a_active, visualize=1")
cmd.do("cafit_orientation TM7a_inactive, visualize=1")
cmd.do("cafit_orientation TM7b_active, visualize=1")
cmd.do("cafit_orientation TM7b_inactive, visualize=1")

# get angle between direction vectors :


cmd.do("angle_between_helices TM3_active, TM3_inactive, method=cafit_orientation")
cmd.do("angle_between_helices TM6a_active, TM6a_inactive, method=cafit_orientation")
cmd.do("angle_between_helices TM7a_active, TM7a_inactive, method=cafit_orientation")
cmd.do("angle_between_helices TM7b_active, TM7b_inactive, method=cafit_orientation")


##     cmd.ray(1500,1500)
#     cmd.png(str(outfile))