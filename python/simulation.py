"""
File:   simulation.py
Name:   Dan Kolbman
Date:   Fall 2013
Description:
        The simulation container for a simulation
"""


import dataIO
import lattice
import boltzmann
import math
import random
import time


def monteCarloStep( pos, jumpSize, size, potRad, radSep ):
	"""
	monterCarloStep : List(Float) Float Float -> List(Float)
	Calculates the next step in the monte carlo simulation.
	Parameters:
		pos - the list of particle positions
		jumpSize - the maximum size of the movement
		size - the size of the box
		potRad - the potential radius
		radSep - the radial separation of two particles
	Returns:
		A new position list of particles
	"""
	# Grab a random particle's position from the position list
	randPart = pos.pop( random.randint(0,len(pos) - 1) )
	# Get old boltzmann factor pair contribution
	oldBFPC = boltzmann.productPairEnergyBoltzmannFactors( pos, randPart, size, potRad, radSep )

	newPos = []
	# Move particle a little in each dimension
	for i in randPart:
		move = i + jumpSize*(random.random() - 0.5) 
		# Account for periodic boundary
		move = move - math.floor(move/size)*size
		newPos.append( move )

	# Calculate new pair energy factors for new position
	newBFPC = boltzmann.productPairEnergyBoltzmannFactors( pos, newPos, size, potRad, radSep )


	# Do monte carlo, compare new Boltzmann factors to old
	if oldBFPC <= 0:
		pos.append( randPart )
		return pos
	elif random.random() < newBFPC/oldBFPC :
		# Move particle
		pos.append( newPos )
		return pos
	else:
		pos.append( randPart )
		return pos
	
	

def runSimulation( nParticles, iterations, freq ):
	"""

	"""
	radSeperation = 0.0968051
	jumpSize  = 0.05
	potentialRange = 0.121006 
	

	# Get an initial lattice placment of particles
	box = lattice.latticeInit( nParticles )

	# Start timer
	timeInit = time.clock()

	for i in range(0, iterations+1):
		box = monteCarloStep( box, jumpSize, 1, potentialRange, radSeperation )
		
		# Write data
		if i%freq == 0:
			dataIO.writePositions( box, 'data/step{}.dat'.format(i) )

	totTime = time.clock() - timeInit
	print('Took:',totTime)

	# End

def main():
	"""

	"""
	nPart = int(input('Number of particles to run: '))	
	iterations = int(input('Number of iterations: '))
	freq = int(input('How often to save state: '))
	print('Beginning...')
	runSimulation( nPart, iterations, freq)


main()









	

