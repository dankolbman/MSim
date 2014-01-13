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
	
def runSimulation(conf, init='' , num=''):
	"""
	runSimulation : Integer Integer Integer -> None
	Run a monte carlo simulation
	
	Parameters:
		nParticles - the number of particles
		iterations - the number of iterations to run for
		freq - how often to save box states
		path - where to save file
		init - the path to an initial box
	"""
	if init != '' and init != 'i' :		# Load in the initial configuration
		box = dataIO.readPositions(conf['initPath'].value)
	else:			# Make a box with a lattice
		# Get an initial lattice placment of particles
		box = lattice.latticeInit(conf['numPart'].value, conf['size'].value)
	# Start timer
	timeInit = time.clock()
	if init == '' or 'i':
		iterations = conf['initIter'].value
	else:
		iterations = conf['iter'].value
	# Run simulation iterations
	for i in range(0, iterations):
		box = monteCarloStep( box,\
					conf['jumpSize'].value,\
					conf['size'].value,\
					conf['potRange'].value,\
					conf['radSep'].value )
		# Write data
		if conf['keep'].value and i%conf['freq'].value == 0:
			dataIO.writePositions( box, conf['path'].value + 'step{}.dat'.format(i))
			print('=> Wrote box to', conf['path'].value + 'step{}.dat'.format(i))
	# Write data
	if init == 'i':		# Record if we're generating an initialbox
		dataIO.writePositions(box, conf['initPath'].value)
		print('=> Saved initial box to', conf['initPath'].value)
	totTime = time.clock() - timeInit
	print('=> Took',totTime,'for simulation')
	print('=> Computing g of r for final step')
	gofr = stats.radDistribution(box, conf['size'].value, 0.005)
	if init != 'i':
		dataIO.writeGofR(gofr, conf['path'].value + 'run{}/gofrFinal.dat'.format(num))
		print('=> Wrote g(r) to', conf['path'].value  + 'run{}/gofrFinal.dat'.format(num))
	print('=> Took',time.clock() - totTime - timeInit, 'for g(r)')
	print('=> Total time:',time.clock()-timeInit)
	return gofr

def avGofR(path):
	#Averages g(r) from different output files.
	subdirs = [sub for sub in os.listdir(path) if os.path.isdir(path + sub)]
	if len(subdirs) > 0:
		print('!! No directories in', path)
		return
	gofrtable = []
	for subdir in subdirs:
		gofrtable.append(stats.readGofR(path + subdir + '/gofrFinal.dat'))
	return stats.averageGofR(gofrtable)

def runExperiment( numSim, path='data/' ):
	"""
	runExperiment : Integer String -> None

	Runs a set of identical simulations a set number of times.

	Parameters:
		numSim - numeber of simulations to run
		path - the path to save the experiment data
	"""
	nPart = int(input('Number of particles to run: '))
	pre = int(input('Initialize box for how many iterations? 0 to generate new every run: '))
	prepath = ''
	iterations = int(input('Number of iterations (excluding initial box): '))
	keep = input('Keep particle position data? (Y/N): ')
	if keep.lower() == "y":
		freq = int(input('How often to save state: '))
	else:
		freq = 0

	if pre > 0:		# Pregenerate a box
		print('Pregenerating a box for', pre, 'steps.')
		timeInit = time.clock()
		runSimulation( nPart, pre, 0, path + 'initial', 'i')
		print('Time to initialize:', time.clock() - timeInit)
		print('==============================================')
		prepath = path + 'initialbox.dat'
	print( 'Beginning Experiment')

	gofrtable = []
	# Run each simulation
	for i in range(0, numSim):
		# Check if the directory already exists
		if not os.path.exists(path+'run{}'.format(i)):
			os.makedirs(path+'run{}'.format(i))
		gofrtable.append(runSimulation( nPart, iterations, freq, path + 'run{}/'.format(i), prepath))
	print('!!!! Going to try to average g(r)')
	gofr = stats.averageGofR(gafrtable)
	print('Saved average g(r) to',path+'avGafR.dat')
	dataIO.writeGofR(gofr, path + 'avGofR.dat')
	print('Done Experiment')

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
