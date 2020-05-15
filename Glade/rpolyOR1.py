#------------------------------------------------------------------------------
#
# Poly resistor Pcell for OpenRule1um
#  by akita11 (20/05/13)
# 
# based on Grade's Poly resistor Pcell example. 
#       Takes 3 parameters - w (width) , r (resistance)
#       and numsegs (number of resistor segments)
#
# Note: The first argument is always the cellView of the subMaster.
#       All subsequent arguments should have default values and will
#       be passed by name
#       This Pcell uses w/l units of metres. This is compatible with schematics
#       where the symbols have values of e.g. w=2u (spice syntax)
#
#------------------------------------------------------------------------------

# Import the db wrappers
from ui import *

# The entry point. The function name *must* match the filename.
def rpolyOR1(cv, w=2e-6, r=100.0, numsegs=1) :
	lib = cv.lib()
	tech = lib.tech()
	dbu = float(cv.dbuPerUU())
	width = int(w * 1.0e6 * dbu )
	res = float(r)

	# Get the rules. Error if they are missing.
	cut_width = tech.getLayerWidth("CNT", "drawing")
	if cut_width <= 0 :
		print "Error: No width rule for layer cont"
		raise NameError
	cut_space = tech.getLayerSpacing("CNT", "drawing")
	if cut_space <= 0 :
		print "Error: No spacing rule for layer cont"
		raise NameError
	poly_width = tech.getLayerWidth("POL", "drawing")
	if poly_width <= 0 :
		print "Error: No width rule for layer polyg"
		raise NameError
	poly_space = tech.getLayerSpacing("POL", "drawing")
	if poly_space <= 0 :
		print "Error: No space rule for layer polyg"
		raise NameError
	poly_to_cut = tech.get2LayerSpacing("CNT", "drawing", "POL", "drawing")
	if poly_to_cut <= 0 :
		print "Error: No space rule for layer cont to layer polyg"
		raise NameError
	poly_ovlp_cut = tech.getLayerEnc("POL", "drawing", "CNT", "drawing")
	if poly_ovlp_cut <= 0 :
		print "Error: No enclosure rule for layer cont by layer polyg"
		raise NameError
#	rpo_ovlp_poly = tech.getLayerEnc("RES", "drawing", "POL", "drawing")
        rpo_ovlp_poly = 0
#	if rpo_ovlp_poly <= 0 :
#		print "Error: No enclosure rule for layer polyg by layer rpo"
#		raise NameError
#	pplus_ovlp_poly = tech.getLayerEnc("nimp", "drawing", "polyg", "drawing")
#	if pplus_ovlp_poly <= 0 :
#		print "Error: No enclosure rule for layer polyg by layer nimp"
#		raise NameError
#	rpo_space_cut = tech.get2LayerSpacing("rpo", "drawing", "cont", "drawing")
        rpo_space_cut = 0
#	if rpo_space_cut <= 0 :
#		print "Error: No space rule for layer rpo to layer cont"
#		raise NameError
	metal_ovlp_cut = tech.getLayerEnc("ML1", "drawing", "CNT", "drawing")
	if metal_ovlp_cut <= 0 :
		print "Error: No enclosure rule for layer cont by layer metal1"
		raise NameError

	# Check width is OK
	if width < poly_width :
		print "Width is less than design rule!"

	# Sheet res in ohms/square
	rho = 20.0
#	bendFactor = 0.56
	
	# length is the length of the resistor body
	length = int(res * width / rho)

	# Create poly
	layer = tech.getLayerNum("POL", "drawing")

	# resistor may have bends - use a path
	bendLength = (poly_space + poly_width) * (numsegs - 1)
        print"bendLength",bendLength
	mainLength = (length - bendLength) / numsegs
        print "mainLength",mainLength
	# Adjust length for centre cut to rpo
	mainLength = mainLength - 2 * (cut_width/2 + rpo_space_cut)
        print "mainLength",mainLength
        # Todo: adjust for number of bends	
	numPoints = numsegs * 2
	xpts = intarray(numPoints)
	ypts = intarray(numPoints)
	i = 0
	while i < numPoints :
		xpts[i]   = width/2 + i * (width + poly_space)
		xpts[i+1] = width/2 + i * (width + poly_space)
		# Alternate the Y points per segment
		if (i/2 % 2) :
			ypts[i]   = width / 2 + mainLength
			ypts[i+1] = width / 2
		else :
			ypts[i]   = width / 2
			ypts[i+1] = width / 2 + mainLength
		i = i + 2

	# Save ptlist
	xsavepts = intarray(numPoints)
	ysavepts = intarray(numPoints)
	for i in range(0, numPoints) :
		xsavepts[i] = xpts[i]
		ysavepts[i] = ypts[i]

	# Extend by halfwidth
	ypts[0] = ypts[0] - width/2
	if numsegs % 2 :
		ypts[numPoints-1] = ypts[numPoints-1] + width/2
	else :
		ypts[numPoints-1] = ypts[numPoints-1] - width/2
	poly = cv.dbCreatePath(xpts, ypts, numPoints, layer, width, 0, 0, 0)
	# Restore ptlist
	for i in range(0, numPoints) :
		xpts[i] = xsavepts[i]
		ypts[i] = ysavepts[i]

        pcont_width = cut_width + poly_ovlp_cut * 2
                
#	# Create N+ layer overlapping poly
#	layer = tech.getLayerNum("nimp", "drawing")
#	pplus_width = width + pplus_ovlp_poly * 2
#	ypts[0] = ypts[0] - (width/2 + pplus_ovlp_poly)
#	if numsegs % 2 :
#		ypts[numPoints-1] = ypts[numPoints-1] + width/2 + pplus_ovlp_poly
#	else :
#		ypts[numPoints-1] = ypts[numPoints-1] - (width/2 + pplus_ovlp_poly)
#	pplus = cv.dbCreatePath(xpts, ypts, numPoints, layer, pplus_width, 0, 0, 0)
	# Restore ptlist
	for i in range(0, numPoints) :
		xpts[i] = xsavepts[i]
		ypts[i] = ysavepts[i]

	# Create poly resistor
	layer = tech.getLayerNum("RES", "drawing")
	rpo_width = width + rpo_ovlp_poly * 2
	ypts[0] = ypts[0] - width/2 + (poly_ovlp_cut + cut_width + rpo_space_cut)
	if numsegs % 2 :
		ypts[numPoints-1] = ypts[numPoints-1] + width/2 - (poly_ovlp_cut + cut_width + rpo_space_cut)
	else :
		ypts[numPoints-1] = ypts[numPoints-1] - width/2 + (poly_ovlp_cut + cut_width + rpo_space_cut)
        rpoly = cv.dbCreatePath(xpts, ypts, numPoints, layer, rpo_width, 0, 0, 0)
	# Restore ptlist
	for i in range(0, numPoints) :
		xpts[i] = xsavepts[i]
		ypts[i] = ysavepts[i]

	# Create contacts
	layer = tech.getLayerNum("CNT", "drawing")
	numCuts = (width + cut_space - 2 * poly_ovlp_cut) / (cut_width + cut_space)
	xoffset = ( width - numCuts * cut_width - (numCuts-1) * cut_space) / 2
	yoffset = poly_ovlp_cut
	for i in range(numCuts) :
		# contacts at start
		cut = Rect(xpts[0]-width/2, ypts[0]-width/2, 
		           xpts[0]-width/2+cut_width, ypts[0]-width/2+cut_width)
		cut.offset(xoffset, yoffset)
#		cv.dbCreateRect(cut, layer)
                cv.dbCreateInst("OpenRule1um_Basic","pcont","layout",
                                Point(xpts[0]-width/2 + pcont_width/2,
                                      ypts[0]-width/2 + pcont_width/2),
                                R0, 1.0)
		# contacts at end
		if numsegs % 2 :
			cut2 = Rect(xpts[numPoints-1]-width/2,           ypts[numPoints-1]+(width/2-cut_width), 
			            xpts[numPoints-1]-width/2+cut_width, ypts[numPoints-1]+width/2)
			cut2.offset(xoffset, -yoffset)
                else :
			cut2 = Rect(xpts[numPoints-1]-width/2,           ypts[numPoints-1]-(width/2-cut_width), 
			            xpts[numPoints-1]-width/2+cut_width, ypts[numPoints-1]-width/2)
			cut2.offset(xoffset, yoffset)
#		cv.dbCreateRect(cut2, layer)
                cv.dbCreateInst("OpenRule1um_Basic","pcont","layout",
                                Point(xpts[numPoints-1]-width/2 + pcont_width/2,
                                      ypts[numPoints-1]-width/2 + pcont_width/2),
                                R0, 1.0)
		xoffset = xoffset + cut_width + cut_space

        # Restore ptlist
	for i in range(0, numPoints) :
		xpts[i] = xsavepts[i]
		ypts[i] = ysavepts[i]

	# Create metal for 1st pin
	layer = tech.getLayerNum("ML1", "drawing")
	met = Rect(xpts[0]-width/2, ypts[0]-width/2, 
	           xpts[0]+width/2, ypts[0]-width/2 + cut_width + metal_ovlp_cut*2)

	plus = cv.dbCreateRect(met, layer)
	net = cv.dbCreateNet("PLUS")
	pin = cv.dbCreatePin("PLUS", net, DB_PIN_INPUT)
	cv.dbCreatePort(pin, plus)

	# Create metal for 2nd pin
	if numsegs % 2 :
		met = Rect(xpts[numPoints-1]-width/2, ypts[numPoints-1] + width/2, 
	                   xpts[numPoints-1]+width/2, ypts[numPoints-1] + width/2 - cut_width - metal_ovlp_cut*2)
	else :
		met = Rect(xpts[numPoints-1]-width/2, ypts[numPoints-1] - width/2, 
	                   xpts[numPoints-1]+width/2, ypts[numPoints-1] - width/2 + cut_width + metal_ovlp_cut*2)

#	xpts[numPoints-1]+width/2, ypts[numPoints-1] + width/2 - cut_width - metal_ovlp_cut*2
	minus = cv.dbCreateRect(met, layer)
	net = cv.dbCreateNet("MINUS")
	pin = cv.dbCreatePin("MINUS", net, DB_PIN_INPUT)
	cv.dbCreatePort(pin, minus)
	
	# Device type
	cv.dbAddProp("type", "res")

	# Update the bounding box
	cv.update()

