#------------------------------------------------------------------------------
#
# RPoly (POL resistor) Pcell for OpenRule1um
#  by akita11 (20/05/11)
# 
# based on Grade's Resistor Pcell for extraction
#
# Note: The first argument is always the cellView of the subMaster.
#       All subsequent arguments should have default values and will
#       be passed by name. Each argument must be seperated by a comma
#	    and whitespace.
#       Note the recognition region point list is always passed in dbu.
#
#------------------------------------------------------------------------------

# Import the db wrappers
from ui import *
from math import *

# The entry point. The function name *must* match the filename.
#
def rpolyOR1_ex(cv, ptlist=[[0,0],[1000,0],[1000,1000],[0,1000]], l=1.0, w=1.0, nsquares=1.0, nbends=0) :
	lib = cv.lib()
	dbu = float(lib.dbuPerUU())
	npts = len(ptlist)

	# Sheet resistance for this resistor in ohms/sq
	rsh = 20.0
	# Number of squares a bend adds
	bendFactor = 1.0

	length = int(l * dbu * 1.0e6)
	width =  int(w * dbu * 1.0e6)
	numBends = nbends

	# Now compute r
	r = rsh * ((length / width) + (numBends * bendFactor))

	# Update the master pcell property.
	# NB dbAddProp will replace an existing property of same name.
	cv.dbAddProp("r", r)
	cv.dbAddProp("w", w / 1.0e-6)
	cv.dbAddProp("l", l / 1.0e-6)

	# Create the recognition region shape
	xpts = intarray(npts)
	ypts = intarray(npts)
	for i in range (npts) :
		xpts[i] = ptlist[i][0]
		ypts[i] = ptlist[i][1]
	# for
	cv.dbCreatePolygon(xpts, ypts, npts, TECH_Y0_LAYER);
	# Create pins
	plus_net = cv.dbCreateNet("A")
	cv.dbCreatePin("A", plus_net, DB_PIN_INPUT)
	minus_net = cv.dbCreateNet("B")
	cv.dbCreatePin("B", minus_net, DB_PIN_INPUT)

	# Set the device modelName property for netlisting
	cv.dbAddProp("modelName", "rppoly")
	
	# Set the netlisting property
	cv.dbAddProp("NLPDeviceFormat", "[@instName] [|A:%] [|B:%] [@modelName] [@w:w=%u] [@l:l=%u] [@r:r=%]")

	# Device type
	cv.dbAddProp("type", "res")

	# Update the bounding box
	cv.update()
#



