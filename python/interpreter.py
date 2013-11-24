"""
File: 	interpreter.py
Author:	Dan Kolbman
Description:
	A user interface for the simulation evironment.
"""
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

	if pre > 0:             # Pregenerate a box
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
		runSimulation( nPart, iterations, freq, path + 'run{}/'.format(i), prepath)
	print('Done Experiment')

def main():
	"""
	Get the path to save experiment data to.
	Run the desired number of experiments
	"""
	print('========================================')
	print('-- Molecular Box Simulator')
	print('----------------------------------------')
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

