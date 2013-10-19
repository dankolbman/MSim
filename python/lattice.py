"""
File:	lattice.py
Name:	Dan Kolbman
Date:	10/11/2013
Description:
	A module for initializing a latice in 3D space.
"""

import math
import dataIO

def latticeInit(n, size=1):
	"""
	Create a lattice with n particles with size size
	
	Parameters:
		n - the number of particles
		size - the size of the lattice (default: 1)
	Returns:
		A position list of all particles
	"""
	# How many particles per side?
	sideNum = math.ceil(n**(1/3))
	latConst = size/sideNum
	# The position list
	positions = []
	numPart = 0
	i = 0
	for i in range(0,sideNum):
		for j in range(0,sideNum):
			for k in range(0,sideNum):
				# If all particles have been added
				#if ( i*sideNum + j*sideNum + k >= n):
				if (numPart >= n):
					break
				else:
					x = i*latConst + 0.5*latConst
					y = j*latConst + 0.5*latConst
					z = k*latConst + 0.5*latConst
					# Append position
					positions.append( [ x, y, z ] )
					numPart += 1
	return positions





