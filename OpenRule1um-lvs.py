# 1um Standard Rule Extraction
# ver0.90 : 2018/4/10: akita11 akita@ifdl.jp

# Initialise boolean package. 
from ui import *
ui = cvar.uiptr
cv = ui.getEditCellView()
geomBegin(cv)
lib = cv.lib()

#print "\n# Loading pcells"
#ui.loadPCell(lib.libName(), "h_nmos_ex")
#ui.loadPCell(lib.libName(), "p_nmos_ex")

print "# Get raw layers"
# Get raw layers
NWL = geomGetShapes("NWL", "drawing")
NWL_dp = geomGetShapes("NWL_dp", "drawing")
DIFF = geomGetShapes("DIFF", "drawing")
POL = geomGetShapes("POL", "drawing")
HPOL = geomGetShapes("HPOL", "drawing")
CNT = geomGetShapes("CNT", "drawing")
ML1 = geomGetShapes("ML1", "drawing")
VIA1 = geomGetShapes("VIA1", "drawing")
ML2 = geomGetShapes("ML2", "drawing")
VIA2 = geomGetShapes("VIA2", "drawing")
ML3 = geomGetShapes("ML3", "drawing")
TEXT = geomGetShapes("TEXT", "drawing")
FRAME = geomGetShapes("FRAME", "drawing")
RES = geomGetShapes("RES", "drawing")
CAP = geomGetShapes("CAP", "drawing")
DIO = geomGetShapes("DIO", "drawing")
Parea = geomGetShapes("Parea", "drawing")
Narea = geomGetShapes("Narea", "drawing")
PAD = geomGetShapes("PAD", "drawing")
DM_dcn = geomGetShapes("DM_dcn", "drawing")
DM_pcn = geomGetShapes("DM_pcn", "drawing")
DM_nscn = geomGetShapes("DM_nscn", "drawing")
DM_pscn = geomGetShapes("DM_pscn", "drawing")
DM_via1 = geomGetShapes("DM_via1", "drawing")
DM_via2 = geomGetShapes("DM_via2", "drawing")

print "# Form derived layers"
PSUB = geomNot(NWL); # psub
#bkgnd     = geomBkgnd()
#PSUB      = geomAndNot(bkgnd, NWL)

GATE = geomAnd(POL, DIFF);
Dif = geomAndNot(DIFF, GATE)
Ndiff = geomAnd(Dif, Narea);
Pdiff = geomAnd(Dif, Parea);
NMOS = geomAnd(GATE, Narea); # nMOS channel
PMOS = geomAnd(GATE, Parea); # pMOS channel
ntap = geomAnd(Ndiff, NWL)
ptap  = geomAnd(Pdiff, PSUB)

print "# Label nodes"
# This must be done BEFORE geomConnect.
geomLabel(POL, "POL", "drawing")
geomLabel(ML1, "ML1", "drawing")
geomLabel(ML2, "ML2", "drawing")
geomLabel(ML3, "ML3", "drawing")

print "# Form connectivity"
geomConnect( [
#        [DM_dcn, Pdiff, ML1],
#        [DM_dcn, Ndiff, ML1],
#        [DM_pcn, POL, ML1],
#        [DM_nscn, NWL, ML1],
#        [DM_nscn, NWL_dp, ML1],
#        [DM_pscn, PSUB, ML1],
#        [DM_via1, ML1, ML2],
#        [DM_via2, ML2, ML3]
        [DM_dcn, Pdiff, ML1],
        [DM_dcn, Ndiff, ML1],
        [DM_pcn, POL, ML1],
        [DM_pcn, POL, POL],
        [DM_nscn, NWL, ML1],
        [DM_nscn, NWL_dp, ML1],
        [DM_pscn, PSUB, ML1],
        [DM_via1, ML1, ML2],
        [DM_via2, ML2, ML3],
        [ptap, Pdiff, PSUB],
        [ntap, Ndiff, NWL]
	     ] )
             
# Save connectivity to extracted view. Saved layers must be
# ones previously connected by geomConnect. Any derived
# layers must be saved to a named layer (e.g. psub below)
print "# Save interconnect"
saveInterconnect([
		NWL,
                PSUB,
		DM_dcn,
		DM_pcn,
		DM_nscn,
		DM_pscn,
		DM_via1,
		DM_via2,
    		[Ndiff, "DIFF"],
		[Pdiff, "DIFF"],
		POL,
		ML1,
		ML2,
		ML3
	     ] )

# Extract MOS devices. Device terminal layers *must* exist in
# the extracted view as a result of saveInterconnect.
# In this case we are using pcell devices which will be
# created according to the recognition region polygon.
print "# Extract MOS devices"
extractMOS("nch", NMOS, POL, Ndiff, PSUB)
extractMOS("pch", PMOS, POL, Pdiff, NWL)

# Extract resistors. Device terminal layers must exist in
# extracted view as a result of saveInterconnect.
#if geomNumShapes(rpo) > 0 :
#	print "# Extract poly resistors"
#	extractRes("rppoly_ex", pres, polyg)

# Extract MOS capacitors. Device terminal layers must exist in
# extracted view as a result of saveInterconnect.
#if geomNumShapes(cap) > 0 :
#	print "# Extract MOS capacitors"
#	extractMosCap("nmoscap_ex", mcap, polyg, active)

print "# Extract parasitics"
# note : These are tentative (un-realistic) parameters (by akita11: 190722)
#extractParasitic(ML1, 0.02e-15, 0.0e-15, "VSS")
#extractParasitic2(ML1, ML2, 0.05e-15, 0.0e-15)
#extractParasitic3D("vss", "vss")

# Exit boolean package, freeing memory
print "# Extraction completed."
geomEnd()

# Open the extracted view
ui.openCellView(lib.libName(), cv.cellName(), "extracted")
