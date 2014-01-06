"""
File:   stats.py
Name:   Dan Kolbman
Date:   Fall 2013
Description:
        A module for initializing a latice in 3D space.
"""

import math
import dataIO

def binCounts( separations, size, resolution ):
	"""
	Create a histogram for particle particle separations
	"""
	bins = []
	width = 0
	# Iterate over each bin
	while width < size/2:
		counts = 0
		# Sort matching elements into bin
		for i in separations:
			if i > width and i <= width + resolution:
				counts += 1
		bins.append( counts )
		# Increase width to next bin
		width += resolution

	return bins

def radDistribution( positions, size, resolution ):
	"""
	Calculate the radial distribution of particles
	"""
	# Number of particles
	numPart = len( positions )
	# The differences in positions
	posDiff = []
	# The radial seperation
	radSep = []
	# Iterate particles
	for i in positions:
		# Iterate again
		for j in positions:
			diff = [0,0,0]
			# Iterate coords
			for coord in range(0,3):
				diff[coord] = i[coord] - j[coord]
				# Apply boundary conditions
				diff[coord] = diff[coord] - size*round(diff[coord]/size)
			posDiff.append(diff)
	
	# Iterate position differences
	for i in posDiff:
		# Seperations
		radSep.append(math.sqrt( i[0]**2 + i[1]**2 + i[2]**2 ))

	# Get shell counts	
	shellCounts = binCounts( radSep, size, resolution )
	

	# Successive shell volumes
	sucShellVol = []

	for i in range(0, int(math.floor( size/(2*resolution) ))):
		sucShellVol.append(4/3 * math.pi * resolution**3 * ((i + 1)**3 - i**3) )

	# Ideal Gas density
	gasDensIdeal = ( numPart - 1 ) / ( size**3 )
	
	# Expected ideal shell counts
	shellCountsIdeal = [ gasDensIdeal*i for i in sucShellVol ]

	# Normalized shell counts
	shellCountsNorm = []
	
	for i in range(0, len(shellCounts)):
		shellCountsNorm.append( ( 2/numPart) * (shellCounts[i] / shellCountsIdeal[i]) - 0.85)

	# G(r) sample
	gofrsample = []
	#                Cast to int might cause problems
	for i in range(0, int( size/(2*resolution))):
			gofrsample.append( [ resolution/2 + i *  resolution, shellCountsNorm[i] ] )
	return gofrsample


def averageGofR( gofrtbl ):
	"""
	Calculate the average g(r) from a table of them
	"""
	gofr = []
	app = gofr.append
	# Iterate each row
	for row in range(0, len(gofrtbl[0])-1):
		suma = 0
		# Iterate each table
		for tbl in range(0, len(gofrtbl)-1):
			# Add the g(r) to total for that row
			suma += gofrtbl[tbl][row][1]
		# Average
		suma = suma / len(gofrtbl)
		app( [ gofrtbl[0][row][0], suma ] )

	return gofr

def test():
	"""
	"""
	pos = dataIO.readPositions('data/experiment1/run1/step0.dat')
	gofr = radDistribution( pos, 1, 0.0005 )
	dataIO.writeGofR(gofr, 'gofr.dat')

