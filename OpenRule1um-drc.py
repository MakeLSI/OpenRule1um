# 1um Standard Rule DRC
# ver1.00 : 2018/2/10: akita11 akita@ifdl.jp
# ver1.01 : 2018/2/23: akita11 akita@ifdl.jp (bug fix)

# simpe function to print # errors - unused.
def printErrors(msg) :
	n = geomGetCount()
	if n > 0 :
		print n, msg

# Initialise DRC package. 
from ui import *
cv = ui().getEditCellView()
geomBegin(cv)

# Get raw layers
NWL = geomGetShapes("NWL", "drawing")
NWL_dp = geomGetShapes("NWL_dp", "drawing")
Pdiff = geomGetShapes("Pdiff", "drawing")
Ndiff = geomGetShapes("Ndiff", "drawing")
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
DM_dcn = geomGetShapes("DM_dcn", "drawing")
DM_pcn = geomGetShapes("DM_pcn", "drawing")
DM_nscn = geomGetShapes("DM_nscn", "drawing")
DM_pscn = geomGetShapes("DM_pscn", "drawing")
DM_via1 = geomGetShapes("DM_via1", "drawing")
DM_via2 = geomGetShapes("DM_via2", "drawing")

# Form derived layers
PSUB = geomNot(NWL); # psub
Diff = geomOr(Pdiff, Ndiff);
NMOS = geomAnd(Pdiff, POL); # nMOS channel
PMOS = geomAnd(Ndiff, POL); # pMOS channel
MOS = geomOr(NMOS, PMOS);

# Form connectivity
geomConnect( [
        [DM_dcn, Pdiff, ML1],
        [DM_dcn, Ndiff, ML1],
        [DM_nscn, NWL, ML1],
        [DM_pscn, PSUB, ML1],
        [DM_via1, ML1, ML2],
        [DM_via2, ML2, ML3],
	     ] )

print "Check GAP"
geomSpace(NWL, 4, "NWL space < 4.0")
geomSpace(NWL_dp, 5, "NWL(diff.pot) space < 5.0")
geomSpace(Pdiff, 1.5, "Pdiff space < 1.5")
geomSpace(Ndiff, 1.5, "Ndiff space < 1.5")
geomSpace(NWL, Ndiff, 3,  "NWL-Ndiff space < 3.0")
geomSpace(Pdiff, DM_nscn, 1.5, "Pdiff-NScont space < 1.5")
geomSpace(Ndiff, DM_pscn, 1.5, "Ndiff-PScont space < 1.5")
geomSpace(POL, 1.0, "POL space < 1.0")
geomSpace(POL, Diff, 0.5, "POL-diff space < 0.5")
geomSpace(MOS, 1, " POL(MOS) space < 1.0")
geomSpace(Diff, DM_dcn, 1, "Diff-dcont space < 1.0")
geomSpace(MOS, DM_dcn, 0.5, "MOS-dcont space < 0.5")
geomSpace(Diff, DM_pcn, 0.5, "Diff-pcont space < 0.5")
geomSpace(POL, DM_pcn, 0.5, "POL-pcont space < 0.5")
geomSpace(ML1, 1, "ML1 space < 1.0")
geomSpace(ML2, 1, "ML2 space < 1.0")
geomSpace(ML3, 1, "ML3 space < 1.0")
geomSpace(ML1, DM_dcn, 1, "ML1-dcont space < 1.0")
geomSpace(ML1, DM_pcn, 1, "ML1-pcont space < 1.0")
geomSpace(ML1, DM_nscn, 1, "ML1-nsubcont space < 1.0")
geomSpace(ML1, DM_pscn, 1, "ML1-psubcont space < 1.0")
geomSpace(ML1, DM_via1, 1, "ML1-via1 space < 1.0") # not shown in rule?
geomSpace(ML2, DM_via1, 1, "ML2-via1 space < 1.0")
geomSpace(ML2, DM_via2, 1, "ML2-via2 space < 1.0") # not shwon in rule?
geomSpace(ML3, DM_via2, 1, "ML3-via2 space < 1.0")

print "Check Overlap"
DM_dcn_r = geomGetRawShapes("DM_dcn", "drawing")
DM_dcn_r_ovlp = geomAnd(DM_dcn_r)
geomArea(DM_dcn_r_ovlp, 0, 0, "dcont overlap")

DM_pcn_r = geomGetRawShapes("DM_pcn", "drawing")
DM_pcn_r_ovlp = geomAnd(DM_pcn_r)
geomArea(DM_pcn_r_ovlp, 0, 0, "pcont overlap")

DM_nscn_r = geomGetRawShapes("DM_nscn", "drawing")
DM_nscn_r_ovlp = geomAnd(DM_nscn_r)
geomArea(DM_nscn_r_ovlp, 0, 0, "nsubcont overlap")

DM_pscn_r = geomGetRawShapes("DM_pscn", "drawing")
DM_pscn_r_ovlp = geomAnd(DM_pscn_r)
geomArea(DM_pscn_r_ovlp, 0, 0, "psubcont overlap")

DM_via1_r = geomGetRawShapes("DM_via1", "drawing")
DM_via1_r_ovlp = geomAnd(DM_via1_r)
geomArea(DM_via1_r_ovlp, 0, 0, "via1 overlap")

DM_via2_r = geomGetRawShapes("DM_via2", "drawing")
DM_via2_r_ovlp = geomAnd(DM_via2_r)
geomArea(DM_via2_r_ovlp, 0, 0, "via2 overlap")

#DM_via1_via2 = geomAnd(DM_via1, DM_via2)
#geomArea(DM_via1_via2, 0, 0, "via1-via2 overlap")
#DM_via1_dcont = geomAnd(DM_via1, DM_dcn)
#geomArea(DM_via1_via2, 0, 0, "via1-dcont overlap")
#DM_via1_pcont = geomAnd(DM_via1, DM_pcn)
#geomArea(DM_via1_via2, 0, 0, "via1-pcont overlap")

print "Check Stacked Con/Via"
geomArea(geomAnd(DM_pcn, DM_via1), 4, 4, "pcont-via1 non-stack")
geomArea(geomAnd(DM_dcn, DM_via1), 4, 4, "dcont-via1 non-stack")
geomArea(geomAnd(DM_via1, DM_via2), 4, 4, "via1-via2 non-stack")

print "Check Width"
geomWidth(NWL,  4, "NWL width < 4.0")
geomWidth(NWL_dp, 4, "NWL(diff.pot) width < 4.0")
geomWidth(Pdiff,  1, "Pdiff width < 1.0")
geomWidth(Ndiff,  1, "Ndiff width < 1.0")
geomWidth(POL,  1, "POL width < 1.0")
geomWidth(ML1, 1, "ML1 width < 1.0")
geomWidth(ML2, 1, "ML2 width < 1.0")
geomWidth(ML3, 1, "ML3 width < 1.0")

print "Check Enclose"
geomEnclose(NWL, Pdiff, 2, "Pdiff enclosure in NWL < 2.0")
geomArea(geomAnd(PSUB, DM_nscn), 0, 0, "nsubcon outside NWL")


print "Check MOS gate extension"
geomExtension(POL, Pdiff, 1, "POL gate extension < 1.0")
geomExtension(POL, Ndiff, 1, "POL gate extension < 1.0")

print "Check stand-alone Cont/Via"
DMcnt1 = geomOr(DM_dcn, DM_pcn)
DMcnt2 = geomOr(DMcnt1, DM_nscn)
DMcnt = geomOr(DMcnt2, DM_pscn)
SAcnt = geomAnd(CNT, geomNot(DMcnt))
geomArea(SAcnt, 0, 0, "Stand alone Cont")
SAvia1 = geomAnd(VIA1, geomNot(DM_via1))
geomArea(SAvia1, 0, 0, "Stand alone VIA1")
SAvia2 = geomAnd(VIA2, geomNot(DM_via2))
geomArea(SAvia2, 0, 0, "Stand alone VIA2")

# Exit DRC package, freeing memory
geomEnd()
#ui().winFit()
