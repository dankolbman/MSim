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
import stats

import math
import random
import time
import os
import gc

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
	
def runSimulation( nParticles, iterations, freq, path ):
	"""
	runSimulation : Integer Integer Integer -> None
	Run a monte carlo simulation
	
	Parameters:
		nParticles - the number of particles
		iterations - the number of iterations to run for
		freq - how often to save box states
		path - where to save file
	"""
	# Pre defined
	radSeperation = 0.0968051
	jumpSize  = 0.05
	potentialRange = 0.121006 
	# Get an initial lattice placment of particles
	box = lattice.latticeInit( nParticles )
	# Start timer
	timeInit = time.clock()
	for i in range(0, iterations):
		box = monteCarloStep( box, jumpSize, 1, potentialRange, radSeperation )
		# Write data
		if freq != 0 and i%freq == 0:
			dataIO.writePositions( box, path + 'step{}.dat'.format(i) )

	totTime = time.clock() - timeInit
	print('Took',totTime,'for simulation')
	print('Computing g of r for final step')
	gofr = stats.radDistribution( box, 1, 0.005 )
	dataIO.writeGofR(gofr, path + 'gofrStep{}.dat'.format(iterations))
	print('Took',time.clock() - totTime - timeInit, 'for g(r)')
	print('Total time:',time.clock()-timeInit)

def runExperiment( numSim, path='data/' ):
	"""
	runExperiment : Integer String -> None

	Runs a set of identical simulations a set number of times.

	Parameters:
		numSim - numeber of simulations to run
		path - the path to save the experiment data
	"""
	nPart = int(input('Number of particles to run: '))	
	iterations = int(input('Number of iterations: '))
	keep = input('Keep particle position data? (Y/N): ')
	if keep.lower() == "y":
		freq = int(input('How often to save state: '))
	else:
		freq = 0

	print( 'Beginning Experiment')

	gofrtable = []
	# Run each simulation
	for i in range(0, numSim):
		# Check if the directory already exists
		if not os.path.exists(path+'run{}'.format(i)):
			os.makedirs(path+'run{}'.format(i))
		runSimulation( nPart, iterations, freq, path + 'run{}/'.format(i))
	
	print( 'Done Experiment' )



def main():
	"""

	"""
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
	


main()

