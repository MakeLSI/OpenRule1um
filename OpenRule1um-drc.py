# 1um Standard Rule DRC
# ver1.00 : 2018/2/10:  akita11 akita@ifdl.jp
# ver1.01 : 2018/2/23:  akita11 akita@ifdl.jp (bug fix)
# ver1.10 : 2018/3/17:  akita11 akita@ifdl.jp (add rules based on rule v110)
# ver1.20 : 2018/4/13:  akita11 akita@ifdl.jp (add rules based on rule v120)
# ver1.30 : 2018/11/27: akita11 akita@ifdl.jp (add rules based for HPOL)
# ver1.31 : 2018/11/28: akita11 akita@ifdl.jp (modified HPOL gap rule)

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

# Form derived layers
PSUB = geomNot(NWL); # psub
Ndiff = geomAnd(DIFF, Narea);
Pdiff = geomAnd(DIFF, Parea);
NMOS = geomAnd(Ndiff, POL); # nMOS channel
PMOS = geomAnd(Pdiff, POL); # pMOS channel
MOS = geomOr(NMOS, PMOS);
HIPOL = geomAnd(HPOL, POL); # HighPolyResistor

# Form connectivity
geomConnect( [
        [DM_dcn, Pdiff, ML1],
        [DM_dcn, Ndiff, ML1],
        [DM_nscn, NWL, ML1],
        [DM_nscn, NWL_dp, ML1],
        [DM_pscn, PSUB, ML1],
        [DM_via1, ML1, ML2],
        [DM_via2, ML2, ML3]
	     ] )

print "Check GAP"
geomSpace(NWL, 4, "NWL space < 4.0")
geomSpace(NWL_dp, 5, "NWL(diff.pot) space < 5.0")
geomSpace(Parea, 0.5, "Parea space < 0.5")
geomSpace(Narea, 0.5, "Narea space < 0.5")
geomSpace(Parea, Narea, 0.5, "Parea-Narea space < 0.5")
geomSpace(DIFF, 1.5, "DIFF space < 1.5")
geomSpace(NWL, Ndiff, 3,  "NWL-Ndiff space < 3.0")
geomSpace(Pdiff, DM_nscn, 0.5, "Pdiff-NScont space < 0.5")
geomSpace(Ndiff, DM_pscn, 1.0, "Ndiff-PScont space < 1.0")
geomSpace(POL, 1.0, "POL space < 1.0")
geomSpace(MOS, 1, " POL(MOS) space < 1.0")
geomSpace(POL, DIFF, 0.5, "POL-diff space < 0.5")
geomSpace(DIFF, DM_dcn, 1, "Diff-dcont space < 1.0")
geomSpace(MOS, DM_dcn, 0.5, "MOS-dcont space < 0.5")
geomSpace(DIFF, DM_pcn, 1.0, "Diff-pcont space < 1.5")
geomSpace(POL, DM_pcn, 0.5, "POL-pcont space < 0.5")
geomSpace(ML1, 1, "ML1 space < 1.0")
geomSpace(ML2, 1, "ML2 space < 1.0")
geomSpace(ML3, 1, "ML3 space < 1.0")
geomSpace(ML1, DM_dcn, 0.5, "ML1-dcont space < 0.5")
geomSpace(ML1, DM_pcn, 0.5, "ML1-pcont space < 0.5")
geomSpace(DM_via1, 0.5, "via1 space < 0.5")
geomSpace(DM_via2, 0.5, "via2 space < 0.5")
#geomSpace(ML1, DM_nscn, 1, "ML1-nsubcont space < 1.0")
#geomSpace(ML1, DM_pscn, 1, "ML1-psubcont space < 1.0")
geomSpace(ML1, DM_via1, 0.5, "ML1-via1 space < 0.5")
geomSpace(ML2, DM_via1, 0.5, "ML2-via1 space < 0.5")
geomSpace(ML2, DM_via2, 0.5, "ML2-via2 space < 0.5")
geomSpace(ML3, DM_via2, 0.5, "ML3-via2 space < 0.5")
geomSpace(DM_via1, DM_dcn, 0.5, "via1-dcont space < 0.5")
geomSpace(DM_via1, DM_pcn, 0.5, "via1-pcont space < 0.5")
geomSpace(DM_via1, DM_nscn, 0.5, "via1-nscont space < 0.5")
geomSpace(DM_via1, DM_pscn, 0.5, "via1-pscont space < 0.5")
geomSpace(DM_via1, DM_via2, 0.5, "via1-via2 space < 0.5")
geomSpace(DM_dcn, 1.0, "dcont space < 1.0")
#geomSpace(HIPOL, 1.0, "Poly in HPOL space < 1.0")
geomSpace(HIPOL, 2.0, "Poly in HPOL space < 2.0")
geomSpace(POL, HIPOL, 1.0, "Poly outside HPOL space < 1.0")

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
geomArea(DM_via1_r_ovlp, 0, 0, "via1 overlap") # not shown in rule v110

DM_via2_r = geomGetRawShapes("DM_via2", "drawing")
DM_via2_r_ovlp = geomAnd(DM_via2_r)
geomArea(DM_via2_r_ovlp, 0, 0, "via2 overlap") # not shown in rule v110

DM_dcn_MOS = geomAnd(DM_dcn, MOS)
geomArea(DM_dcn_MOS, 0, 0, "dcn-MOS overlap")

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
geomWidth(Parea,  0.5, "Parea width < 0.5")
geomWidth(Narea,  0.5, "Narea width < 0.5")
geomWidth(DIFF,  1.0, "DIFF width < 1.0")
geomWidth(POL,  1, "POL width < 1.0")
geomWidth(ML1, 1, "ML1 width < 1.0")
geomWidth(ML2, 1, "ML2 width < 1.0")
geomWidth(ML3, 1, "ML3 width < 1.0")
geomWidth(HIPOL, 2.0, "Poly in HPOL width < 2.0")

## ToDo: check HIPOL length (20-80um) (181127:akita11)

print "Check Enclose"
geomEnclose(NWL, Pdiff, 2, "Pdiff enclosure in NWL < 2.0")
geomArea(geomAnd(PSUB, DM_nscn), 0, 0, "nsubcon outside NWL") # not shown in rule v110
geomEnclose(Parea, DIFF, 0.5, "DIFF enclosure in Parea < 0.5")
geomEnclose(Narea, DIFF, 0.5, "DIFF enclosure in Narea < 0.5")
geomEnclose(HPOL, HIPOL, 5.0, "POL enclosure in HPOL < 5.0")

print "Check MOS gate extension"
geomExtension(POL, DIFF, 1, "POL gate extension < 1.0")

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
