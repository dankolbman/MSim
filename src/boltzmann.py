"""
File:   boltzmann.py
Name:   Dan Kolbman
Date:   Fall 2013
Description:
	Boltzmann
"""

import math

def productPairEnergyBoltzmannFactors( positions, part, size, potRad, radSep ):
	"""
	
	Parameters:
		pos - the list of positions to test
		part - the particle position to test
		potRad - the potential radius
		radSep - the radial separation of two particles
	Returns:
		The Boltzmann factor
	"""
	withinPot = []
	for pos in positions:
		dx = part[0] - pos[0]
		dy = part[1] - pos[1]
		dz = part[2] - pos[2]
		
		# Periodic boundaries
		dx = dx - size*round(dx/size)
		dy = dy - size*round(dy/size)
		dz = dz - size*round(dz/size)
		"""
		if dx > size/2:
			dx = dx - size
		elif dx <= -size/2:
			dx = dx + size
		if dy > size/2:
			dy = dy - size
		elif dy <= -size/2:
			dy = dy + size
		if dz > size/2:
			dz = dz - size
		elif dz <= -size/2:
			dz = dz + size
		"""
		dist =  math.sqrt(dx*dx + dy*dy + dz*dz)
		# Append to list if in range
		if  dist < potRad*2 and dist > 0:
			withinPot.append(pos)
			if dist < radSep:
				# Within core, boltzmann factor = 0
				return 0
	
	# Return if nothing within potential
	if withinPot == []:
		# Boltzmann factor = 1
		return 1

	# For hard shell
	return 1

