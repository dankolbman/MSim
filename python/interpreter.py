"""
File: 	interpreter.py
Author:	Dan Kolbman
Description:
	A user interface for the simulation environment.
"""
import time
import os
import simulation as sim
import stats
import dataIO

class Setting():
	"""
	A Class for holding configuration settings.
	Properties
	- Name - the setting name
	- Value - the value of the setting
	- type - the type of the value stored
	- desc - description
	"""
	__slots__ = ('name','value','type','desc')

def mkSetting(conf, name, value, type, desc=''):
	""" Constructor for Setting type """
	nSetting = Setting()
	nSetting.name = name
	nSetting.value = value
	nSetting.type = type
	nSetting.desc = desc
	# Assign the setting to the dictionary
	conf[name] = nSetting
	return nSetting

##### End class definitions

def runExperiment(conf):
	"""
	runExperiment : Configuration(dict) -> None
	Runs a set of identical simulations a set number of times.
	Parameters:
		conf - the configuration
	"""
	prepath = ''
	# Pregenerate a box if needed
	if conf['initIter'].value > 0:
		print('=> Pregenerating a box for', conf['initIter'].value, 'steps.')
		timeInit = time.clock()
		# Calling the simulation function
		# TODO: Only pass conf
		sim.runSimulation( conf, 'i')
		print('=> Time to initialize:', time.clock() - timeInit)
		prepath = conf['path'].value + 'initialbox.dat'
		print('=> Saved initial box to', prepath)
	
	print('---------------------------')
	print('=> Beginning Experiment:')
	gofrtable = []
	# Run each simulation
	for i in range(0, conf['numSim'].value):
		print('---------------------------')
		print('=> Running Simulation',i)
		# Check if the directory already exists
		if not os.path.exists(conf['path'].value + 'run{}'.format(i)):
			print('=> Making new directory:', 'run{}.dat'.format(i))
			os.makedirs(conf['path'].value + 'run{}'.format(i))

		gofrtable.append(sim.runSimulation( conf, prepath))
	print('=> Done Experiment')
	print('Try to average gofr')
	gofr = stats.averageGofR(gofrtable)
	print('Saved average g(r) to',conf['path'].value+'avGafR.dat')
	dataIO.writeGofR(gofr, conf['path'].value + 'avGofR.dat')
			

def assignSetting(conf, string):
	""" assignSetting : Dict(Setting) String -> None
	Assigns a value to a setting and handles errors.
	Based on a 'setting value' string input'
	"""
	cmd = string.split()
	try:
		# Attempts to cast to the proper type
		conf[cmd[0]].value = conf[cmd[0]].type(cmd[1])
	except KeyError:	# The setting does not exist
		print('!!', cmd[0], 'is not a property.')
	except ValueError:	# The user tried to enter a different type than expected
		print('!! Could not assign. Was expecting type', conf[cmd[0]].type)

def defaultConfig():
	"""Returns the default configuration dictionary."""
	conf = dict()
	mkSetting(conf,'freq',1000,int,'The number of iterations between state saves')
	mkSetting(conf,'initIter',10000,int,'The number of iterations used to create an itial box')
	mkSetting(conf,'initPath','data/init.dat',str,'The path to save the initial box to')
	mkSetting(conf,'iter',5000,int,'The number of iterations to run each simulation for in\n\
			addition to the number used for the initial box.')
	mkSetting(conf,'keep',False,bool,'Whether or not to save inbetween box states,\n\
			0 = False, true otherwise')
	mkSetting(conf,'numPart',400,int,'The number of particles to run')
	mkSetting(conf,'numSim',1,int,'The number of simulations to run')
	mkSetting(conf,'path', 'data/', str,'The path to save data output to')
	mkSetting(conf,'radSep', 0.0968051, float,'The radial separaration')
	mkSetting(conf,'potRange', 0.121006, float,'The potential range')
	mkSetting(conf,'jumpSize', 0.05, float,'The jump size used to move a particle every step')
	
	return conf

def printConfig(conf):
	""" Prints the configuration output to terminal"""
	print('== Current Configuration ==')
	for key in conf:
		print('--', key, '=', conf[key].value) # Debug:,'\t',type(conf[key].value))
	print('===========================')

def printHelp(conf):
	""" Prints commands and properties """
	print('== Available Commands ==')
	print('-- config - display current config')
	print('-- help - display this output')
	print('-- property value - change that property in the config')
	print('-- run - run simulation(s) with current config')
	print('========================')
	print('Configuration properties:')
	for key in conf:
		print('--', key, '\t', conf[key].desc)
	print('========================')
	
def main():
	"""
	Main program loop
	Displays title and enters a terminal interface.
	User can enter commands here and run simulations.
	"""
	# Load a default configuration
	conf = defaultConfig()
	print('========================================')
	print('-------- Molecular Box Simulator -------')
	print('----------------------------------------')
	printConfig(conf)
	print('-- For a list of commands, enter "help"')
	running = True
	# Terminal loop
	while running:
		cmd = input('> ')
		cmdLower = cmd.lower()#.split()
		if cmdLower == 'exit':
			running = False
		elif cmdLower == 'config':
			printConfig(conf)
		elif cmdLower == 'help':
			printHelp(conf)
		elif len(cmd.split()) > 1:
			assignSetting(conf, cmd)	
		elif cmdLower == 'run':
			runExperiment(conf)
		else:
			print('Command not found. Type \'exit\' to exit')

if __name__ == '__main__':
	main()
