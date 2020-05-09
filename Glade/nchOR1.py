#------------------------------------------------------------------------------
#
# nMOS Pcell for OpenRule1um
#  by akita11 (20/05/06)
# 
# based on Grade's NMOS Pcell example. 
#	    Create a Pcell with parameters w (width of gate),
#	    l (length of gate), nf (number of gate fingers).
#
# Note: The first argument is always the cellView of the subMaster.
#       All subsequent arguments should have default values and will
#       be passed by name. Each argument should be seperated by a comma
#	    and whitespace. 
#       This Pcell uses w/l units of metres. This is compatible with schematics
#       where the symbols have values of e.g. w=2u (spice syntax)
#
#------------------------------------------------------------------------------

# Import the db wrappers
from ui import *
#import pdb; pdb.set_trace()

# The entry point. The function name *must* match the filename.
def nchOR1(cv, w=2e-6, l=1e-6, nf=1, polyCnt=0, leftCnt=1, rightCnt=1) :
	lib = cv.lib()
	tech = lib.tech()
	dbu = float(cv.dbuPerUU())
	width = int(w * 1.0e6 * dbu )
	length = int(l * 1.0e6 * dbu )
	fingers = int(nf)

       	# Get the rules. Error if they are missing.
	cut_width = tech.getLayerWidth("CNT", "drawing")
	if cut_width <= 0 :
		print "No width rule for layer cont"
		return
	cut_space = tech.getLayerSpacing("CNT", "drawing")
	if cut_space <= 0 :
		print "No spacing rule for layer cont"
		return
	pwell_ovlp_active = tech.getLayerEnc("DM_PSUB", "drawing", "DIFF", "drawing")
	if pwell_ovlp_active <= 0 :
		print "No enclosure rule for layer od by layer psub"
		return
	poly_to_cut = tech.get2LayerSpacing("CNT", "drawing", "POL", "drawing")
	if poly_to_cut <= 0 :
		print "No space rule for layer cont to layer polyg"
		return
	active_ovlp_cut = tech.getLayerEnc("DIFF", "drawing", "CNT", "drawing")
	if active_ovlp_cut <= 0 :
		print "No enclosure rule for layer cont by layer od"
		return
        poly_ovlp_active = tech.getLayerExt("POL", "drawing", "DIFF", "drawing")
	if poly_ovlp_active <= 0 :
		print "No extension rule for layer od by layer poly"
		return	
	poly_ovlp_cut = tech.getLayerEnc("POL", "drawing", "CNT", "drawing")
	if poly_ovlp_cut <= 0 :
		print "No enclosure rule for layer cont by layer polyg"
		return
	nplus_ovlp_active = tech.getLayerEnc("Narea", "drawing", "DIFF", "drawing")
	if nplus_ovlp_active <= 0 :
		print "No enclosure rule for layer od by layer nimp"
		return
	metal_ovlp_cut = tech.getLayerEnc("ML1", "drawing", "CNT", "drawing")
	if metal_ovlp_cut <= 0 :
		print "No enclosure rule for layer cont by layer metal1"
		return
	poly_via_size = cut_width + 2 * poly_ovlp_cut
	poly_via_neck_offset = poly_via_size / 2 - length / 2

	# Create active
	od = tech.getLayerNum("DIFF", "drawing")
	height = active_ovlp_cut*2 + cut_width*(fingers + 1) + poly_to_cut*2*fingers + length*fingers
	r = Rect(-height/2, -width/2, height/2, width/2)
	active = cv.dbCreateRect(r, od);

	# Create pwell / substrate
	pwell = tech.getLayerNum("DM_PSUB", "drawing")
	r.bias(pwell_ovlp_active)
	pwell = cv.dbCreateRect(r, pwell);
	net = cv.dbCreateNet("B")
	pin = cv.dbCreatePin("B", net, DB_PIN_INPUT)
	cv.dbCreatePort(pin, pwell)

	# Create nplus
	nimp = tech.getLayerNum("Narea", "drawing")
	r = Rect(-height/2 - nplus_ovlp_active, 
		 -width/2 - nplus_ovlp_active, 
		 height/2 + nplus_ovlp_active,
		 width/2 + nplus_ovlp_active)
	cv.dbCreateRect(r, nimp);

	# Create poly fingers
	poly = tech.getLayerNum("POL", "drawing")
	cont = tech.getLayerNum("CNT", "drawing")
	metal1 = tech.getLayerNum("ML1", "drawing")
	xoffset = active_ovlp_cut + cut_width + poly_to_cut -height/2
	for i in range(fingers) :
#                print"xoffset",xoffset,"polyCnt",polyCnt
		p = Rect(xoffset, 
			-width/2 -poly_ovlp_active,
			xoffset + length,
			width/2 + poly_ovlp_active)
		gate = cv.dbCreateRect(p, poly)
		net = cv.dbCreateNet("G")
		pin = cv.dbCreatePin("G", net, DB_PIN_INPUT)
		if polyCnt :
			numCuts = length / (cut_width + cut_space)
                        xoffset2 = xoffset
                        #xoffset = active_ovlp_cut + cut_width + poly_to_cut -height/2
#                        print"xoffset2",xoffset,"length",length
			if width < poly_via_size :
				q = Rect(xoffset2 - poly_via_neck_offset,
					 width/2 + poly_ovlp_active,
					 xoffset2 + length + poly_via_neck_offset,
					 width/2 + poly_ovlp_active + poly_via_size)
				cv.dbCreateRect(q, poly)
				metpin = cv.dbCreateRect(q, metal1)
				cv.dbCreatePort(pin, metpin)
                                yoffset = width/2 + poly_ovlp_active + poly_ovlp_cut + cut_width/2
                                cv.dbCreateInst("OpenRule1um_Basic","pcont","layout", Point(xoffset2 + length/2/2, yoffset),R0, 1.0)
			else :
				q = Rect(xoffset2,
					 width/2 + poly_ovlp_active,
					 xoffset2 + length,
                                         width/2 + poly_ovlp_active + poly_via_size)
                                yoffset = width/2 + poly_ovlp_active + poly_ovlp_cut + cut_width/2
                                cv.dbCreateRect(q, poly)
                                cv.dbCreateInst("OpenRule1um_Basic","pcont","layout", Point(xoffset2 + length/2, yoffset),R0, 1.0)
				metpin = cv.dbCreateRect(q, metal1)
				cv.dbCreatePort(pin, metpin)
			xfudge = (length - numCuts * (cut_width + cut_space)) / 2
			xoffset2 = active_ovlp_cut + cut_width + poly_to_cut + poly_ovlp_cut + xfudge -height/2
			for j in range(numCuts) :
				r = Rect(xoffset2,
				 	width/2 + poly_ovlp_active + poly_ovlp_cut,
				 	xoffset2 + cut_width,
				 	width/2 + poly_ovlp_active + poly_ovlp_cut + cut_width)
#				cv.dbCreateRect(r, cont)
				xoffset2 = xoffset2 + cut_width + cut_space
		else :
			cv.dbCreatePort(pin, gate)
		xoffset = xoffset + length + 2*poly_to_cut + cut_width
                
        # Create S/D contacts
	cont = tech.getLayerNum("CNT", "drawing")
	numCuts = (width - 2*active_ovlp_cut + cut_space) / (cut_width + cut_space)
	yfudge = (width - numCuts * (cut_width + cut_space)) / 2
	xoffset = active_ovlp_cut - height/2
#	xoffset = active_ovlp_cut + cut_width/2 - height/2
	for i in range(fingers+1) :
		yoffset = active_ovlp_cut + yfudge -width/2 
#		yoffset = active_ovlp_cut + cut_width/2 + yfudge -width/2 
                # don't draw: (l==0 && i==0) || (r==0 && i==fingers)
                # -> draw: (l==1&&i==0) || (r==0&&i==finger) || (0<i<fingers)
#                print "i=",i,"fingers=",fingers
                if ((leftCnt == 1 and i == 0)
                    or (rightCnt == 1 and i == fingers)
                    or ((i > 0) and (i < fingers))):
#                        print "draw"
		        for j in range(numCuts) :
#			cut = Rect(0, 0, cut_width, cut_width)
#			cut.offset(xoffset, yoffset)
#			cv.dbCreateRect(cut, cont)
                                cv.dbCreateInst("OpenRule1um_Basic","dcont","layout", Point(xoffset + cut_width/2, yoffset + cut_width/2),R0, 1.0)
			        yoffset = yoffset + cut_width + cut_space
		xoffset = xoffset + length + 2*poly_to_cut + cut_width
			
	# Create metal
	metal1 = tech.getLayerNum("ML1", "drawing")
	xoffset = active_ovlp_cut - metal_ovlp_cut - height/2
	for i in range(fingers+1) :
		met = Rect(0, -width/2, cut_width + 2*metal_ovlp_cut, width/2)
		met.offset(xoffset, 0)
		if (i+1) % 2 :
			source = cv.dbCreateRect(met, metal1)
			net = cv.dbCreateNet("S")
			pin = cv.dbCreatePin("S", net, DB_PIN_INOUT)
			cv.dbCreatePort(pin, source)
		else :
			drain = cv.dbCreateRect(met, metal1)
			net = cv.dbCreateNet("D")
			pin = cv.dbCreatePin("D", net, DB_PIN_INOUT)
			cv.dbCreatePort(pin, drain)
		xoffset = xoffset + length + 2*poly_to_cut + cut_width
	
	# Device type
	cv.dbAddProp("type", "mos")

	# Update the bounding box
	cv.update()

