"""
File:   simulation.py
Name:   Dan Kolbman
Description:
	Provides a front end for the user to input parameters and run
	experiments.
"""
import math
import random
import time
import os
import gc
from subprocess import call

import dataIO
import lattice
import boltzmann
import stats

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
	
def runSimulation(conf):
	"""
	runSimulation : conf(dict) -> None
	Run a monte carlo simulation
	"""
	if conf['useInit'].value:		# Load in the initial configuration
		print('=> Reading initial position file')
		box = dataIO.readPositions(conf['initPath'].value)
	else:				# Make a box with a lattice
		# Get an initial lattice placment of particles
		print('=> Generating a lattice')
		box = lattice.latticeInit(conf['numPart'].value, conf['size'].value)
		print('=> Initializing lattice for', conf['initIter'].value,'steps')
		# Call to C g(r) function
		for i in range(0, conf['initIter'].value):
			box = monteCarloStep( box,\
					conf['jumpSize'].value,\
					conf['size'].value,\
					conf['potRange'].value,\
					conf['radSep'].value )
		# Write data
		dataIO.writePositions( box, conf['initPath'].value)
		print('=> Wrote initial box to', conf['initPath'].value)
	print('=> Running simulation for',conf['iter'].value,'steps')
	# Start timer
	timeInit = time.clock()
	# Run simulation iterations
	for i in range(1, conf['iter'].value+1):
		box = monteCarloStep( box,\
					conf['jumpSize'].value,\
					conf['size'].value,\
					conf['potRange'].value,\
					conf['radSep'].value )
		# Write data
		if i%conf['freq'].value == 0:
			dataIO.writePositions( box, conf['path'].value + 'step{}.pos'.format(i))
			### Evaluate g(r)
			print('=> Wrote box to', conf['path'].value + 'step{}.pos'.format(i))
			print('=> Calling g(r) program')
			call(['./gr',\
				str(conf['path'].value + 'step{}.pos'.format(i)),\
				str(conf['path'].value + 'grstep{}.dat'.format(i)),\
				str(conf['numPart'].value),\
				str(conf['size'].value),\
				str(conf['numBins'].value) ])
			print('=> Wrote g(r) to', conf['path'].value + 'gr{}.dat'.format(i))
	totTime = time.clock() - timeInit
	print('=> Took',totTime,'for', conf['iter'].value, 'steps')
	print('=> Averageing g(r)')
	timeInit = time.clock()
	stats.avGofR(conf)

def main():
	"""
	!!!!!!!!!!
	LEGACY CODE
	interpreter.py should be used for the user interface

	Get the path to save experiment data to.
	Run the desired number of experiments
	"""
	print('WARNING!!!\nDid you mean to run interpreter.py?')
	path = input("Path to save experiment session? (Default data/): ")
	if path == "":
		path = "data/"
	numExp  = 1
	while (numExp > 0 ):
		numSim = int(input('Number of simulations to run: '))
		runExperiment( numSim, path +'experiment{}/'.format(numExp) )
		if input('Do another experiment? (Y/N): ').lower() == 'n':
			numExp = -1
		numExp += 1

if __name__ == '__main__':
	main()
